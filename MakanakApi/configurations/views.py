from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from  Api.MakanakModels.models import *
from django.contrib.auth.models import Group, User

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        data['user_id'] = self.user.id
#         data['groups'] = self.user.groups.values_list('name', flat=True)
        data['role'] = Group.objects.get(user=self.user.id).name
        data['name']=UserProfile.objects.get(user_id=self.user.id).first_name
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer