from django.urls import path

from .views import (
    UserListAPIView, UserCreateAPIView,
    UserDetailAPIView, UserDeleteAPIView,
    UpdateAPIView,
    ResetPasswordConfirm, ResetPasswordCheck, ResetPasswordRequestToken, ChangePasswordAPI,
)


urlpatterns = [
    path('', UserListAPIView.as_view(), name='user-list'),
    path('create', UserCreateAPIView.as_view(), name='user-creator'),
    path('profile/<int:pk>/', UserDetailAPIView.as_view(), name='user-profile'),
    path('delete/<int:pk>/', UserDeleteAPIView.as_view(), name='user-destroyer'),
    path('update/<int:pk>/', UpdateAPIView.as_view(), name='user-updater'),
    path('update_password/', ChangePasswordAPI.as_view(),
         name='user-change-password'),

    path('confirm/', ResetPasswordConfirm.as_view(),
         name="reset-password-confirm"),
    path('check/', ResetPasswordCheck.as_view(), name="reset-password-check"),
    path('resetpasswordtoken/', ResetPasswordRequestToken.as_view(),
         name="reset-password-request"),
]
