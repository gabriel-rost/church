from django.contrib import admin

from .models import (
    Post,
    Archive,
    Comment,
    Content,
    Profile,
    Channel,
)

admin.site.register(Post)
admin.site.register(Archive)
admin.site.register(Comment)
admin.site.register(Content)
admin.site.register(Profile)
admin.site.register(Channel)
