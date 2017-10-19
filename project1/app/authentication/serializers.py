from rest_framework import serializers
from authentication.models import Account
from rest_framework.validators import ValidationError

from django.core.validators import MinLengthValidator


class AccountSerializer(serializers.ModelSerializer):
    """
    This Account Serializer allow to CRUD (CREATE READ UPDATE DELETE) the fields: id, email, first name,
    last name, password, confirm_password.
    Create a new user and update user information.
    """
    password = serializers.CharField(write_only=True, required=True, validators=[MinLengthValidator(8)])
    confirm_password = serializers.CharField(write_only=True, required=True, validators=[MinLengthValidator(8)])

    class Meta:
        model = Account
        fields = ('email', 'first_name', 'last_name', 'password',
                  'confirm_password', 'identifier', 'is_superuser', 'created_at', 'updated_at')
        read_only_fields = ('identifier', 'is_superuser', 'created_at', 'updated_at')


class AccountSerializerLogin(serializers.BaseSerializer):

    def to_representation(self, instance):

        if isinstance(instance, dict):
            return {
                'email': instance["account"].email,
                'identifier': str(instance["account"].identifier),
                'first_name': instance["account"].first_name,
                'last_name': instance["account"].last_name,
                'is_superuser': instance["account"].is_superuser,
                'token': instance["token"]
            }
        elif isinstance(instance, Account):
            return {
                'email': instance.email,
                'identifier': instance.identifier,
                'first_name': instance.first_name,
                'last_name': instance.last_name,
                'is_superuser': instance.is_superuser
            }
        else:
            return {
                'email': instance.user.email,
                'identifier': instance.user.identifier,
                'first_name': instance.user.first_name,
                'last_name': instance.user.last_name,
                'is_superuser': instance.user.is_superuser
            }


class PasswordSerializer(serializers.ModelSerializer):
    # change password serializer
    password = serializers.CharField(write_only=True, required=True, validators=[MinLengthValidator(8)])
    confirm_password = serializers.CharField(write_only=True, required=True, validators=[MinLengthValidator(8)])

    class Meta:
        model = Account
        fields = ('password', 'confirm_password',)
        read_only_fields = ()


class EmailSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        pass

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def to_internal_value(self, data):
        email = data.get('email')

        # Perform the data validation.
        if not email:
            raise ValidationError({
                'message': 'This field is required.'
            })

        # Return the validated values. This will be available as
        # the `.validated_data` property.
        return {
            'email': email
        }


class PasswordResetSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        pass

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def to_internal_value(self, data):
        token = data.get('token')
        password = data.get('password')
        confirm_password = data.get('email')

        # Perform the data validation.
        if not token:
            raise ValidationError({
                'message': 'This field is required.'
            })
        if not password:
            raise ValidationError({
                'message': 'This field is required.'
            })
        if not confirm_password:
            raise ValidationError({
                'message': 'This field is required.'
            })

        # Return the validated values. This will be available as
        # the `.validated_data` property.
        return {
            'token': token,
            'password': password,
            'confirm_password': confirm_password
        }

