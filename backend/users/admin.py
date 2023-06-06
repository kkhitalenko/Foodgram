from django.contrib import admin
from users.models import Subscription, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'first_name', 'last_name')
    list_filter = ('email', 'username')


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'author')


admin.site.register(User, UserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
