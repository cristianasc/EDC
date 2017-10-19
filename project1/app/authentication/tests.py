from collections import OrderedDict

from django.test import TestCase
from authentication.models import Account
from rest_framework.test import APIClient


class AuthenticationTestCase(TestCase):
    def setUp(self):
        Account.objects.create(email='test@test.com', first_name='unit', last_name='test')

    def test_account_details(self):
        account = Account.objects.get(email='test@test.com')
        self.assertEqual(account.email, 'test@test.com')
        self.assertEqual(account.first_name, 'unit')
        self.assertEqual(account.last_name, 'test')

    def test_create_account(self):
        user = Account.objects.get(email='test@test.com')
        user.is_superuser = True
        user.save()

        client = APIClient()
        client.force_authenticate(user=user)

        """
        List the accounts created so far and the only one will be the account created in the setUp method.
        """

        url = "/api/accounts/" # endpoint to list the users
        response = client.get(url)
        # parse the response and assert if the result is equal to what we expect
        rsp = response.data["results"]
        del rsp[0]['updated_at']
        del rsp[0]['created_at']
        del rsp[0]['identifier']
        self.assertEqual(rsp, [OrderedDict([('email', u'test@test.com'), ('first_name', u'unit'), ('last_name', u'test'), ('is_superuser', True)])])

        # now let's make the user a normal user
        user.is_staff = False
        user.save()

        # let's create a new account -- account 2
        url = "/api/accounts/"
        data = {'email': 'test1@test.com', 'password': '12345678','confirm_password': '12345678', 'first_name': 'unit', 'last_name': 'test',}
        response = client.post(path=url, data=data, format='json')
        new_user_identifier = response.data["identifier"]
        self.assertEqual(response.status_code, 201)

        # change password of other user; that can't be possible
        url = "/api/change_password/"+str(new_user_identifier)+"/"
        data = {'password': '1234', 'confirm_password': '1234'}
        response = client.put(url, data)
        self.assertEqual(response.status_code, 403)  # it fails, it's forbidden
        self.assertEqual(response.data, {u'detail': u'You do not have permission to perform this action.'})

        # change password with the current user
        url = "/api/change_password/"+user.identifier+"/"
        data = {'password': '1234', 'confirm_password': '1234'}
        response = client.put(url, data)
        self.assertEqual(response.data, {'status': 'Bad Request', 'message': {
            'confirm_password': [u'Ensure this value has at least 8 characters (it has 4).'],
            'password': [u'Ensure this value has at least 8 characters (it has 4).']}})
        self.assertEqual(response.status_code, 400)

        # change correctly the password
        url = "/api/change_password/"+user.identifier+"/"
        data = {'password': '123456789', 'confirm_password': '123456789'}
        response = client.put(url, data)
        self.assertEqual(response.data, {'status': 'Updated', 'message': 'Account updated.'})
        self.assertEqual(response.status_code, 200)

        # get informations
        url = "/api/accounts/"
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

        url = "/api/accounts/"+str(new_user_identifier)+"/"
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        rsp = dict(response.data)
        del rsp['updated_at']
        del rsp['created_at']
        del rsp['identifier']
        self.assertEqual(rsp, {'first_name': u'unit', 'last_name': u'test', 'is_superuser': False,'email': u'test1@test.com'})

        url = "/api/accounts/"+user.identifier+"/"
        data = {'email': 'test2@test.com', 'first_name': 'unit', 'last_name': 'test',}
        response = client.put(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(dict(response.data), {'status': 'Updated', 'message': 'Account updated.'})

        url = "/api/accounts/"+user.identifier+"/"
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        rsp = dict(response.data)
        del rsp['updated_at']
        del rsp['created_at']
        del rsp['identifier']
        self.assertEqual(rsp, {'first_name': u'unit', 'last_name': u'test', 'is_superuser': True, 'email': u'test2@test.com'})

        url = "/api/accounts/"+user.identifier+"/"
        response = client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'status': 'Deleted', 'message': 'The account has been deleted.'})

        url = "/api/accounts/"+user.identifier+"/"
        response = client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, {u'detail': u'Not found.'})

        client.login(email='test@test.com')
        client.logout()

        client.force_authenticate(user=None)

        url = "/api/create_civilian/"
        data = {'email': 'test7@test.com', 'password': '123456789', 'confirm_password': '123456789',
                'first_name': 'unit2', 'last_name': 'test2'}
        response = client.post(path=url, data=data, format='json')
        print response.data
        self.assertEqual(response.status_code, 201)