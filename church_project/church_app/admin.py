from django.contrib import admin

# Register your models here.
from church_app.models import *
x = [Post, Archive, Comment, Content, Profile, Channel]
admin.site.register(x)