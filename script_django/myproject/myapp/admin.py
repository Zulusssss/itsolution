from django.contrib import admin
from .models import TextRequest

@admin.register(TextRequest)
class TextRequestAdmin(admin.ModelAdmin):
    list_display = ('text', 'created_at')

