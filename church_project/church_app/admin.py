from django.contrib import admin

from .models import (
    Post,
    Archive,
    Comment,
    Content,
    Profile,
    Channel,
    ReadingPlan,
    PlanTask,
    Chapter,
    Book,
    Verse,
)

admin.site.register(Post)
admin.site.register(Archive)
admin.site.register(Comment)
admin.site.register(Content)
admin.site.register(Profile)
admin.site.register(Channel)
admin.site.register(ReadingPlan)
admin.site.register(PlanTask)

admin.site.site_header = "Administração Church App"
admin.site.site_title = "Painel de Administração"
admin.site.index_title = "Painel de Administração do Clube de Leitura"