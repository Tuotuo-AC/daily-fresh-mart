from django.contrib import admin
from .models import Profile, Address

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'mobile', 'email_active', 'nickname')
    search_fields = ('user__username', 'mobile')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'receiver', 'mobile', 'province', 'city', 'district', 'is_default')
    list_filter = ('province', 'city')
    search_fields = ('receiver', 'mobile')
