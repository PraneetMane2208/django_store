from django.contrib import admin
from .models import Tag

@admin.register(Tag)
# Register your models here.
class TagAdmin(admin.ModelAdmin):
    search_fields=['label']