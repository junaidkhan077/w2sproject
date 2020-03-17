from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Province(models.Model):
    id = models.AutoField("id", primary_key=True, unique=True)
    name = models.CharField("name", max_length=100, null=True,blank=True)
    created_by = models.IntegerField("Created By", null=True,blank=True)
    created_at = models.DateTimeField("Created At", null=True,blank=True)
    modified_by = models.IntegerField("Modified By", null=True,blank=True)
    modified_at = models.DateTimeField("Modified At", null=True,blank=True)

    class Meta:
        db_table = "Province_Mstr"

    def __str__(self):
        return self.id

class City(models.Model):
    id = models.AutoField("id", primary_key=True, unique=True)
    province = models.ForeignKey(Province,related_name="province_id",on_delete=models.CASCADE)
    name = models.CharField("name", max_length=100, null=True, blank=True)
    created_by = models.IntegerField("Created By", null=True, blank=True)
    created_at = models.DateTimeField("Created At", null=True, blank=True)
    modified_by = models.IntegerField("Modified By", null=True, blank=True)
    modified_at = models.DateTimeField("Modified At", null=True, blank=True)

    class Meta:
        db_table = "City_Mstr"

    def __str__(self):
        return self.id

class UserProfile(models.Model):
    id = models.AutoField("id", primary_key=True, unique=True)
    user = models.ForeignKey(User,related_name='User_id', on_delete=models.CASCADE)
    first_name = models.CharField("first_name", max_length=100, null=True,blank=True)
    last_name = models.CharField("last_name",max_length=100,blank=True,null=True)
    primary_email = models.CharField("primary_email",max_length=50,blank=True,null=True)
    secondary_email = models.CharField("secondary_email",max_length=50,blank=True,null=True)
    primary_phone = models.CharField("primary_phone",max_length=50,blank=True,null=True)
    secondary_phone = models.CharField("secondary_phone",max_length=50,blank=True,null=True)
    business_name = models.CharField("business_name",max_length=200,blank=True,null=True)
    address1 = models.TextField("address1",blank=True,null=True)
    address2 = models.TextField("address2",blank=True,null=True)
    city = models.CharField("city",max_length=50,blank=True,null=True)
    province = models.CharField("Province",max_length=50,blank=True,null=True)
    country = models.CharField("country",max_length=50,blank=True,null=True)
    postalcode = models.CharField("postalcode", max_length=20, blank=True, null=True)
    id_proof = models.FileField(upload_to='documents/')
    is_approved = models.BooleanField("is_approved",blank=True,null=True)
    is_lock = models.BooleanField("is_lock",blank=True,null=True)
    allow_notifications = models.BooleanField("allow_notifications",blank=True,null=True)
    fb_auth_token = models.TextField("fb_auth_token",blank=True,null=True)
    created_by = models.IntegerField("Created By", null=True, blank=True)
    created_at = models.DateTimeField("Created At", null=True, blank=True)
    modified_by = models.IntegerField("Modified By", null=True, blank=True)
    modified_at = models.DateTimeField("Modified At", null=True, blank=True)

    class Meta:
        db_table = "UserProfile"

    def __str__(self):
        return self.id

