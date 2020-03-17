from django.contrib import admin
from Api.Users.models import ResetPasswordToken


@admin.register(ResetPasswordToken)
class ResetPasswordTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'key', 'created_at', 'used',
                    'expired', 'ip_address', 'user_agent')
