from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Subscription, User


@admin.register(User)
class MyUserAdmin(UserAdmin):
    list_display = (
        'username', 'first_name', 'last_name', 'email',
    )
    search_fields = (
        'username', 'email',
    )
    list_filter = (
        'first_name', 'email',
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'author',
    )
