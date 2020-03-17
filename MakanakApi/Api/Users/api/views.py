import time
from django.conf import settings
import coreapi
import random
from datetime import timedelta
from django.utils import timezone
from rest_framework.generics import (
    ListAPIView, CreateAPIView, RetrieveUpdateAPIView,
    RetrieveAPIView, DestroyAPIView
)

from rest_framework import parsers, renderers, status
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema
from Api.Users.models import ResetPasswordToken
from Api.Users.api.signals import reset_password_token_created, pre_password_reset, post_password_reset
from Api.Users.api.utils import get_client_masked_ip

from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework import pagination
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated)
from .serializers import UserSerializer, User, EmailSerializer, PasswordTokenSerializer, TokenSerializer, UserOneSerializer
from django.http import HttpResponse, JsonResponse


class UserListAPIView(ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = UserSerializer

    def get_queryset(self, *args, **kwargs):
        queryset_list = User.objects.all()

        page_size = 'page_size'
        if self.request.GET.get(page_size):
            pagination.PageNumberPagination.page_size = self.request.GET.get(
                page_size)
        else:
            pagination.PageNumberPagination.page_size = 10
        query = self.request.GET.get('q')
        if query:
            queryset_list = queryset_list.filter(
                Q(email__icontains=query) |
                Q(username__icontains=query)
            )

        return queryset_list.order_by('-id')


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = User.objects.all()
    # serializer_class = UserProfileSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    # queryset = UserProfile.objects.all()


class UserDetailAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDeleteAPIView(DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer


class UpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class ChangePasswordAPI(RetrieveUpdateAPIView):

    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UserOneSerializer

    def post(self, serializer):
        from django.contrib.auth.hashers import check_password
        import json
        datas = self.request.data
        old_password_entered = datas['old_password']
        new_password = datas['new_password']
        email = datas['user_email']
        user = User.objects.filter(email=email)
        user = UserOneSerializer(user, many=True)
        if len(user.data) == 0:
            msg = {
                "detail": "User not exist for this email",
                "status": "False"
            }
            return JsonResponse({"detail": "User not exist for this email", "status": "success"})
        old_password = user.data[0]['password']
        print(old_password)

        matchcheck = check_password(old_password_entered, old_password)
        print(matchcheck)
        if matchcheck:
            instance = User.objects.get(email=email)
            instance.set_password(new_password)
            instance.save()

            return JsonResponse({"detail": "Password Changed", "status": "success"})
        else:
            return JsonResponse({"detail": "Current password is wrong", "status": "fail"})


User = get_user_model()


def get_password_reset_token_expiry_time(is_long_token=False):
    """
    Returns the password reset token expirty time in hours (default: 24)
    Set Django SETTINGS.DJANGO_REST_MULTITOKENAUTH_RESET_TOKEN_EXPIRY_TIME to overwrite this time
    :return: expiry time
    """

    if is_long_token:
        return getattr(settings, 'DJANGO_REST_MULTITOKENAUTH_RESET_TOKEN_LONG_EXPIRY_TIME', 48)

    # get token validation time
    return getattr(settings, 'DJANGO_REST_MULTITOKENAUTH_RESET_TOKEN_EXPIRY_TIME', 24)


def get_use_username():
    """
    Returns if user search need to be based on username instead of email
    Set Django SETTINGS.DJANGO_REST_MULTITOKENAUTH_USE_USERNAME to overwrite this
    :return: use username
    """
    return getattr(settings, 'DJANGO_REST_MULTITOKENAUTH_USE_USERNAME', False)


def get_new_token(user, request):
    """
    Return new reset password token
    """
    return ResetPasswordToken.objects.create(
        user=user,
        user_agent=request.META['HTTP_USER_AGENT'],
        ip_address=get_client_masked_ip(request)
    )


def filter_parameters_from_token(token_input):
    if token_input and '?' in token_input:
        token_input = token_input.split('?')[0]

    return token_input


class ResetPasswordConfirm(APIView):
    """
    An Api View which provides a method to reset a password based on a unique token
    """
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser,
                      parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = PasswordTokenSerializer

    schema = AutoSchema(
        manual_fields=[
            coreapi.Field('password', location='body', required=True),
            coreapi.Field('token', location='body', required=True),
        ]
    )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data['password']
        token = filter_parameters_from_token(
            serializer.validated_data['token'])

        # get token validation time

        # find token
        reset_password_token = ResetPasswordToken.objects.filter(
            key=token, used=False).first()

        if reset_password_token is None:
            return Response({'error': 'token not found'}, status=status.HTTP_404_NOT_FOUND)

        password_reset_token_validation_time = get_password_reset_token_expiry_time(
            is_long_token=reset_password_token.is_long_token
        )

        # check expiry date
        expiry_date = reset_password_token.created_at + timedelta(
            hours=password_reset_token_validation_time)
        if timezone.now() > expiry_date:
            # mark token as expired
            reset_password_token.expired = True
            reset_password_token.used = True
            reset_password_token.save()
            return Response({'error': 'token expired'}, status=status.HTTP_400_BAD_REQUEST)

        # change users password
        if reset_password_token.user.has_usable_password():
            pre_password_reset.send(
                sender=self.__class__, user=reset_password_token.user, request=request)
            reset_password_token.user.set_password(password)
            reset_password_token.user.save()
            post_password_reset.send(
                sender=self.__class__, user=reset_password_token.user, request=request)

        # Mark token as used
        ResetPasswordToken.objects.filter(
            user=reset_password_token.user).update(used=True)

        return Response()


class ResetPasswordCheck(APIView):
    """
    An Api View which provides a method to check that a token is valid.
    """
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser,
                      parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = TokenSerializer

    schema = AutoSchema(
        manual_fields=[
            coreapi.Field('token', location='body', required=True),
        ]
    )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = filter_parameters_from_token(
            serializer.validated_data['token'])

        # get token validation time

        # find token
        reset_password_token = ResetPasswordToken.objects.filter(
            key=token, used=False).first()

        if reset_password_token is None:
            return Response({'error': 'token not found'}, status=status.HTTP_404_NOT_FOUND)

        password_reset_token_validation_time = get_password_reset_token_expiry_time(
            is_long_token=reset_password_token.is_long_token
        )

        # check expiry date
        expiry_date = reset_password_token.created_at + timedelta(
            hours=password_reset_token_validation_time)

        if timezone.now() > expiry_date:
            # mark token as expired
            reset_password_token.expired = True
            reset_password_token.used = True
            reset_password_token.save()
            return Response({'error': 'token expired'}, status=status.HTTP_400_BAD_REQUEST)

        return Response()


class ResetPasswordRequestToken(APIView):
    """
    An Api View which provides a method to request a password reset token based on an e-mail address

    Sends a signal reset_password_token_created when a reset token was created
    """
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser,
                      parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = EmailSerializer

    schema = AutoSchema(
        manual_fields=[
            coreapi.Field('email', location='body',
                          required=True, type='email'),
        ]
    )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        # find a user by email address (case insensitive search)
        if get_use_username():
            users = User.objects.filter(username__iexact=email)
        else:
            users = User.objects.filter(email__iexact=email)

        active_user_found = False

        # iterate over all users and check if there is any user that is active
        # also check whether the password can be changed (is useable), as there could be users that are not allowed
        # to change their password (e.g., LDAP user)
        for user in users:
            if user.is_active and user.has_usable_password():
                active_user_found = True

        print(not active_user_found)
        # No active user found, raise a validation error
        if not active_user_found:
            # time.sleep(random.randint(500, 2000) / 1000)
            return Response({'error': 'No active email Id'}, status=status.HTTP_400_BAD_REQUEST)

        # last but not least: iterate over all users that are active and can change their password
        # and create a Reset Password Token and send a signal with the created token
        for user in users:
            if user.is_active and user.has_usable_password():
                # define the token as none for now
                token = None

                # check if the user already has a token
                if user.password_reset_tokens.filter(expired=False, used=False).count() > 0:
                    # yes, already has a token, re-use this token
                    token = user.password_reset_tokens.all()[0]

                    # get token validation time
                    password_reset_token_validation_time = get_password_reset_token_expiry_time(
                        is_long_token=token.is_long_token
                    )

                    expiry_date = token.created_at + timedelta(
                        hours=password_reset_token_validation_time)

                    if timezone.now() > expiry_date:
                        token.expired = True
                        token.used = True
                        token.save()

                        token = get_new_token(user, request)

                else:
                    # no token exists, generate a new token
                    token = get_new_token(user, request)
                # send a signal that the password token was created
                # let whoever receives this signal handle sending the email for the password reset
                reset_password_token_created.send(
                    sender=self.__class__,
                    reset_password_token=token,
                    request=request
                )
        # done
        return Response()
