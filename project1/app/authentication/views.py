import json

from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets, views, status, permissions, models, serializers
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from .permissions import IsAccountOwner, MustBeSuperUser
from .models import Account
from .serializers import AccountSerializer, PasswordSerializer, AccountSerializerLogin


class AccountViewSet(viewsets.ModelViewSet):
    """
    ## List users
    - #### Method: **GET**
    - #### URL: **/api/accounts/**
    - #### Permissions: **Must be super user**
    ## Create an user
    - #### Method: **POST**
    - #### URL: **/api/accounts/**
    - #### Parameters: email, first_name, last_name, password, confirm_password
    - #### Permissions: **Must be super user**
    ## Update an user
    - #### Method: **PUT**
    - #### URL: **/api/accounts/&lt;identifier&gt;/**
    - #### Parameters: email, first_name, last_name
    - #### Permissions: **Is Authenticated and Is Account Owner**
    ## Delete an user
    - #### Method: **DELETE**
    - #### URL: **/api/accounts/&lt;identifier&gt;/**
    - #### Permissions: **Is Authenticated and (Is Account Owner or Super User)**
    """
    lookup_field = 'identifier'
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_permissions(self):
        """
        Any operation is permitted only if the user is Authenticated.
        The create method is permitted only too if the user is Authenticated.
        Note: The create method isn't a SAFE_METHOD

        -> Permissions
        # list
            Must be super user
        # create
            Allow any
        # destroy and update
            Is Authenticated and Is Account Owner

        :return:
        :rtype:
        """
        if self.request.method == 'POST':
            return permissions.AllowAny(), \
                   MustBeSuperUser(message="In order to create a new account we must be a super user!"),

        if self.request.method in permissions.SAFE_METHODS:
            return permissions.AllowAny(), \
                   MustBeSuperUser(message="In order to create a new account we must be a super user!"),

        return permissions.IsAuthenticated(), IsAccountOwner()

    def list(self, request, *args, **kwargs):
        """
        B{List} users
        B{URL:} ../api/accounts/
        """
        MustBeSuperUser(user=request.user, message='You don\'t have permissions to see this list!')

        return super(AccountViewSet, self).list(self, request, *args, **kwargs)

    def create(self, request):
        """
        B{Create} an user
        B{URL:} ../api/accounts/

        :type  email: str
        :param email: email
        :type  first_name: str
        :param first_name: The first name of user
        :type  last_name: str
        :param last_name: The last name of user
        :type  password: str
        :param password: The password of user
        :type  confirm_password: str
        :param confirm_password: The password confirmation
        """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            if serializer.validated_data["password"] != serializer.validated_data["confirm_password"]:
                return Response({'status': 'Bad Request',
                                 'message': {
                                     "Password": "Doesn't match!"
                                 }
                                 }, status=status.HTTP_400_BAD_REQUEST)

            instance = Account.objects.create_user(**serializer.validated_data)
            serializer = AccountSerializerLogin(instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({'status': 'Bad Request',
                         'message': serializer.errors
                         }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = get_object_or_404(Account.objects.all(), identifier=kwargs.get('identifier', ''))

        self.check_object_permissions(self.request, instance)

        serializer = self.serializer_class(instance, data=request.data, partial=True)

        if serializer.is_valid():
            instance.email = request.data.get('email', instance.email)
            instance.first_name = request.data.get('first_name', instance.first_name)
            instance.last_name = request.data.get('last_name', instance.last_name)

            instance.save()

            return Response({'status': 'Updated',
                             'message': 'Account updated.'
                             }, status=status.HTTP_200_OK)

        return Response({'status': 'Bad Request',
                         'message': serializer.errors
                         }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(Account.objects.all(), identifier=kwargs.get('identifier', ''))
        self.check_object_permissions(self.request, instance)
        instance.delete()
        return Response({'status': 'Deleted',
                         'message': 'The account has been deleted.'
                         }, status=status.HTTP_200_OK)


class AccountChangePassword(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    ## Change password
    - #### Method: **PUT**
    - #### URL: **/api/change_password/&lt;identifier&gt;/**
    - #### Parameters: Password and confirm_password
    - #### Permissions: **Is Authenticated and Is Account Owner**
    """
    lookup_field = 'identifier'
    queryset = Account.objects.all()
    serializer_class = PasswordSerializer

    def get_permissions(self):
        return permissions.IsAuthenticated(), IsAccountOwner()

    def update(self, request, *args, **kwargs):
        """
        B{Update} the password
        B{URL:} ../api/change_password/<identifier>/

        -> Permissions
        # update
            UserIsUser

        :type  password: str
        :param password: The password
        :type  confirm_password: str
        :param confirm_password: The confirmation password
        """
        instance = get_object_or_404(Account.objects.all(), identifier=kwargs.get('identifier', ''))

        self.check_object_permissions(self.request, instance)

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            password = request.data.get('password', None)
            confirm_password = request.data.get('confirm_password', None)

            if password and confirm_password and password == confirm_password:
                instance.set_password(password)
                instance.save()

            return Response({'status': 'Updated',
                             'message': 'Account updated.'
                             }, status=status.HTTP_200_OK)

        return Response({'status': 'Bad Request',
                         'message': serializer.errors
                         }, status=status.HTTP_400_BAD_REQUEST)


class AccountCreateCivilian(views.APIView):

    def post(self, request):
        serializer = AccountSerializer(data=request.data)

        if serializer.is_valid():
            if serializer.validated_data["password"] != serializer.validated_data["confirm_password"]:
                return Response({'status': 'Bad Request',
                                 'message': {
                                     "Password": "Doesn't match!"
                                 }
                                 }, status=status.HTTP_400_BAD_REQUEST)

            instance = Account.objects.create_civilian(**serializer.validated_data)
            serializer = AccountSerializerLogin(instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({'status': 'Bad Request',
                         'message': serializer.errors
                         }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(views.APIView):
    """
    ## Login to the platform
    - #### Method: **POST**
    - #### Parameters: **email, password**
    - #### URL: **/api/auth/login/**
    - #### Permissions: **Allow any**
    """
    def post(self, request):
        """
        B{Login} an user
        B{URL:} ../api/auth/login/
        """
        data = json.loads(request.body)
        email = data.get('email', None)
        password = data.get('password', None)

        # get user
        accounts = Account.objects.filter(email=email)
        if accounts.count() == 0:
            return Response({'status': 'Unauthorized',
                             'message': 'Email and/or password is wrong.'
                             }, status=status.HTTP_401_UNAUTHORIZED)

        account = authenticate(identifier=accounts[0].identifier, password=password)

        if account is not None:
            if account.is_active:
                token = Token.objects.get(user=account)

                serialized = AccountSerializerLogin({"account": account,
                                                    "token": token.key})

                return Response(serialized.data)

            else:
                return Response({'status': 'Unauthorized',
                                 'message': 'This account has been disabled.'
                                 }, status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response({'status': 'Unauthorized',
                             'message': 'Email and/or password is wrong.'
                             }, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(views.APIView):
    """
    ## Logout from the platform
    - #### Method: **POST**
    - #### URL: **/api/auth/logout/**
    - #### Permissions: **Is authenticated**
    """
    def get_permissions(self):
        return permissions.IsAuthenticated(),

    def post(self, request):
        """
        B{Logout} an user
        B{URL:} ../api/auth/logout/
        """
        logout(request)

        return Response({}, status=status.HTTP_204_NO_CONTENT)


class MyDetails(views.APIView):
    """
    ## See the details of the current logged user
    - #### Method: **GET**
    - #### URL: **/api/me/**
    - #### Permissions: **Is authenticated**
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_permissions(self):
        return permissions.IsAuthenticated(),

    def get(self, request):
        """
        See the details of the current logged user
        B{URL:} ../api/me/
        """
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)
