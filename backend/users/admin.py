from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Subscription, User


@admin.register(User)
class MyUserAdmin(UserAdmin):
    list_display = (
        'username', 'first_name', 'last_name', 'email',
        'recipes_count', 'followers_count',
    )
    search_fields = (
        'username', 'email',
    )
    list_filter = (
        'first_name', 'email',
    )

    def recipes_count(self, obj):
        return obj.recipes.count()

    def followers_count(self, obj):
        return obj.subscribing.count()
    
    recipes_count.short_description = 'Всего рецептов'
    followers_count.short_description = 'Всего подписчиков'


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'author',
    )
