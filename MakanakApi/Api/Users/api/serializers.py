from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.translation import ugettext_lazy as _


User = get_user_model()



class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordTokenSerializer(serializers.Serializer):
    password = serializers.CharField(label=_("Password"), style={
                                     'input_type': 'password'})
    token = serializers.CharField()


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_staff', ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        phone = validated_data['phone']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        business_name = validated_data['business_name']
        email_address = validated_data['email_address']
        address1 = validated_data['address1']
        address2 = validated_data['address2']
        city = validated_data['city']
        state = validated_data['state']
        country = validated_data['country']
        zip_code = validated_data['zip_code']
        secondary_email = validated_data['secondary_email']

        user_obj = User(
            username=email,
            email=email,
            is_staff=True
        )
        user_obj.set_password(password)
        user_obj.save()

        return validated_data

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        return instance


class UserOneSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
