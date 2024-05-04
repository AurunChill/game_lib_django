from django.contrib import admin
from django.utils.safestring import mark_safe

# Project
from app_users import models


@admin.register(models.UserModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", 'show_avatar', "first_name", "last_name", "email",]
    search_fields = ["username", "first_name", "last_name", "email",]
    readonly_fields=['show_avatar_big']
    fields = ('username', 'email', 'password', 'image', 'show_avatar_big')
    save_on_top = True

    @admin.display(description='Аватар')
    def show_avatar(self, user: models.UserModel):
        if user.image:
            return mark_safe(f'<img src="{user.image.url}" style="border-radius: 10px" width=35>')
        return 'Нет аватарки'
    
    @admin.display(description='Аватар (Фото)')
    def show_avatar_big(self, user: models.UserModel):
        if user.image:
            return mark_safe(f'<img src="{user.image.url}" style="border-radius: 10px" width=250>')
        return 'Нет аватарки'