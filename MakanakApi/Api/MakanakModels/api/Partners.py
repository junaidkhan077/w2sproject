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

from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated)
from django.http import HttpResponse, JsonResponse
from .serializers import *
from Api.MakanakModels.models import *
import datetime
from django.db import transaction
from django.contrib.auth.models import Group, User





class CreatePartnersApiView(CreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PartnersSerializer

    def post(self,request, *args, **kwargs):

        req_data=self.request.data
        print(req_data)
        try:
            sid = transaction.savepoint()
            user_id = self.request.user.id

            first_name = req_data['first_name']
            last_name = req_data['last_name']
            primary_email = req_data['primary_email'].strip()
            # secondary_email = req_data['secondary_email']
            primary_phone = req_data['primary_phone']
            # secondary_phone = req_data['secondary_phone']
            business_name = req_data['business_name']
            address1 = req_data['address1']
            address2 = req_data['address2']
            city_id = req_data['city']
            province_id = req_data['province']
            is_approved = req_data['is_approved']
            is_lock = req_data['is_lock']
            allow_notifications = req_data['allow_notifications']
            username = req_data['username'].strip()
            password = 'Smile@2019'
            postalcode=req_data['postalcode']
            country = req_data['country']


            if not User.objects.filter(username = username).exists():


                user_obj = User(
                    username=username,
                    email=primary_email,
                )
                user_obj.set_password(password)
                user_obj.save()

                usr_id = user_obj.pk

                role_id = Group.objects.get(name='Partners').id
                user = User.objects.get(id=usr_id)
                group = Group.objects.get(id=role_id)
                user.groups.add(group)

                BusinessPartners = UserProfile(
                first_name=first_name,
                last_name = last_name,
                primary_email = primary_email,
                # secondary_email = secondary_email,
                primary_phone = primary_phone,
                # secondary_phone = secondary_phone,
                business_name = business_name,
                address1 = address1,
                address2 = address2,
                city = city_id,
                province = province_id,
                is_approved = is_approved,
                is_lock = is_lock,
                allow_notifications = allow_notifications,
                user_id =usr_id,
                created_at= datetime.datetime.now(),
                created_by = user_id,
                postalcode=  postalcode,
                country =country
                )
                BusinessPartners.save()

                data = {
                    'status': 'success',
                    'message': 'Business partners created successfully',
                }

                transaction.savepoint_commit(sid)
            else:

                data = {
                    'status': 'failure',
                    'message': 'Business partners email address already exists',
                }

        except Exception as error:
            transaction.savepoint_rollback(sid)
            data = {
                'status': 'failure',
                'message': str(error),
            }

        return JsonResponse({'data': data})


class UpdatePartnersApiView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PartnersSerializer

    def post(self,request, *args, **kwargs):

        req_data=self.request.data

        try:
            sid = transaction.savepoint()
            user_id = self.request.user.id

            first_name = req_data['first_name']
            last_name = req_data['last_name']
            primary_email = req_data['primary_email'].strip()
            # secondary_email = req_data['secondary_email']
            primary_phone = req_data['primary_phone']
            # secondary_phone = req_data['secondary_phone']
            business_name = req_data['business_name']
            address1 = req_data['address1']
            address2 = req_data['address2']
            city_id =req_data['city']
            province_id = req_data['province']
            is_approved = req_data['is_approved'],
            is_lock = req_data['is_lock']
            allow_notifications = req_data['allow_notifications']
            usr_id =req_data['user_id']
            username = req_data['username'].strip()
            postalcode = req_data['postalcode']
            country = req_data['country']
            # password = 'Smile@2019'


            if UserProfile.objects.filter(user_id=usr_id).exists():

                # user_obj = User.objects.get(id=user_id)
                # user_obj.username=username
                # user_obj.email=primary_email
                #
                # user_obj.save()

                BusinessPartners = UserProfile.objects.get(user_id = usr_id)
                BusinessPartners.first_name=first_name
                BusinessPartners.last_name = last_name
                BusinessPartners.primary_email = primary_email
                # BusinessPartners.secondary_email = secondary_email
                BusinessPartners.primary_phone = primary_phone
                # BusinessPartners.secondary_phone = secondary_phone
                BusinessPartners.business_name = business_name
                BusinessPartners.address1 = address1
                BusinessPartners.address2 = address2
                BusinessPartners.city_id = city_id
                BusinessPartners.province_id = province_id
                # BusinessPartners.is_approved = is_approved
                # BusinessPartners.is_lock = is_lock
                # BusinessPartners.allow_notifications = allow_notifications
                BusinessPartners.modified_at = datetime.datetime.now()
                BusinessPartners.modified_by = user_id
                BusinessPartners.postalcode = postalcode
                BusinessPartners.country = country
                BusinessPartners.save()

                data = {
                    'status': 'success',
                    'message': 'Business partners info updated successfully',
                }



            else:

                data = {
                    'status': 'failure',
                    'message': 'Business partners does not exists',
                }

        except Exception as error:
            transaction.savepoint_rollback(sid)
            data = {
                'status': 'failure',
                'message': str(error),
            }
        transaction.savepoint_commit(sid)
        return JsonResponse({'data': data})


class PartnersListApiView(ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PartnersSerializer

    def get(self,request, *args, **kwargs):

        user_id = self.request.user.id
        role = Group.objects.get(user=user_id)
        partner_id = self.kwargs["user_id"]
        try:
            # if role.name.lower() == 'admin':
              if partner_id==0:
                  UserList = User.objects.filter(groups__name='partners')
                  List=[]
                  for val in UserList:
                      id =User.objects.get(username=val).pk
                      List.append(id)

                  PartnersList = UserProfile.objects.filter(user_id__in=List)
                  PartnersList = PartnersSerializer(PartnersList, many=True)
              else:
                  print(partner_id,'i d')
                  PartnersList = UserProfile.objects.get(user_id=partner_id)
                  PartnersList = PartnersSerializer(PartnersList,many=False)

              data = {
                  'data' : PartnersList.data,
                  'status': 'success',
                  'message': 'data retrieved successfully',
              }
            # else :
            #     data = {
            #         'status': 'failure',
            #         'message': 'User doesn''t have access',
            #     }

        except Exception as error:
            data = {
                'status': 'failure',
                'message': str(error),
            }
        return JsonResponse({'Resp': data})




class UserProfileApiView(ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PartnersSerializer

    def get(self,request, *args, **kwargs):

        user_id = self.request.user.id
        role = Group.objects.get(user=user_id)
        try:

            PartnersList = UserProfile.objects.get(user_id=user_id)
            PartnersList = PartnersSerializer(PartnersList,many=True)

            data = {
            'data' : PartnersList.data,
            'status': 'success',
            'message': 'data retrieved successfully',
            }


        except Exception as error:
            data = {
                'status': 'failure',
                'message': str(error),
            }
        return JsonResponse({'Resp': data})


class DeleteUserApiView(DestroyAPIView):
        permission_classes = [IsAuthenticatedOrReadOnly]
        serializer_class = PartnersSerializer

        def get(self, request, *args, **kwargs):

            user_id = self.request.user.id
            role = Group.objects.get(user=user_id)
            userid = self.kwargs["user_id"]
            try:

                Profile = UserProfile.objects.get(user_id=userid)
                Profile.delete()

                role = Group.objects.get(user=userid)
                role_id = Group.objects.get(name=role.name).id
                user = User.objects.get(id=userid)
                group = Group.objects.get(id=role_id)
                user.groups.remove(group)

                obj = User.objects.get(id=userid)
                obj.delete()

                data = {
                    'status': 'success',
                    'message': 'user data deleted successfully',
                }


            except Exception as error:
                data = {
                    'status': 'failure',
                    'message': str(error),
                }
            return JsonResponse({'Resp': data})
