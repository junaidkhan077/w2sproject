from django.urls import path

from .Partners import *


urlpatterns = [
    path('CreatePartners', CreatePartnersApiView.as_view(),
         name='Createpartners'),
    path('UpdatePartners', UpdatePartnersApiView.as_view(),
         name='updatepartners'),
    path('PartnersList/<int:user_id>',
         PartnersListApiView.as_view(), name='PartnersList'),
    path('UserProfile', UserProfileApiView.as_view(), name='UserProfile'),

    path('DeleteUser/<int:user_id>', DeleteUserApiView.as_view(),
         name='DeleteUser'),


]
