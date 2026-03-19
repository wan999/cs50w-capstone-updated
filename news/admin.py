from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Category, Article, Comment, Avatar, Favorite

# Register your models here.
admin.site.register(User, UserAdmin)

admin.site.register(Category)

admin.site.register(Article)

admin.site.register(Comment)

admin.site.register(Avatar)

admin.site.register(Favorite)