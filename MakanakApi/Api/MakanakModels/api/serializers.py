from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models import CharField, Value as V
from django.db.models.functions import Concat
from django.db.models import Q
from django.contrib.auth.models import Group, User
from Api.MakanakModels.models import *
User = get_user_model()



class PartnersSerializer(serializers.ModelSerializer):

    role = serializers.SerializerMethodField("GetRoleName")
    # province_name = serializers.SerializerMethodField("GetStateName")
    # city_name = serializers.SerializerMethodField("GetCityName")
    username = serializers.SerializerMethodField("GetUserName")
    class Meta:
        model = UserProfile
        fields = ['user_id','first_name','last_name','primary_email','secondary_email','primary_phone','secondary_phone',
        'business_name' ,'address1','address2','city','province','country','id_proof','is_approved',
        'is_lock','allow_notifications','role','postalcode','username']


    def GetRoleName(self, UserProfile):
        RoleName = Group.objects.get(user=UserProfile.user_id).name
        return RoleName

    def GetUserName(self,UserProfile ):
        username =User.objects.get(id=UserProfile.user_id).username
        return username
    # def GetStateName(self,UserProfile):
    #     StateName = Province.objects.get(id=UserProfile.province).name
    #     return StateName
    #
    # def GetCityName(self,UserProfile):
    #     CityName = City.objects.get(id=UserProfile.city).name
    #     return CityName



