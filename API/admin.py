from django.contrib import admin
from django.db import models
from .models import Author

# Register your models here.


class AuthorAdmin(admin.ModelAdmin):
    list_display=('name', 'auth_user')


admin.site.register(Author, AuthorAdmin)