from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser


@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    list_display = (
        'username', 'first_name', 'last_name', 'email',
    )
    fields = (
        ('username', 'email', ),
        ('first_name', 'last_name', ),
    )
    fieldsets = []
    search_fields = (
        'username', 'email',
    )
    list_filter = (
        'first_name', 'email',
    )
