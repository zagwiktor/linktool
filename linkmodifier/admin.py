from django.contrib import admin
from .models import *
# Register your models here.
class LinkAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Link, LinkAdmin)


