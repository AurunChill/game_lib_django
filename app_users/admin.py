from django.contrib import admin

# Project
from app_users import models


@admin.register(models.UserModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name", "email",]
    search_fields = ["username", "first_name", "last_name", "email",]

    