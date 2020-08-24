from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    list_filter = ('author', )
    search_fields = ('title', 'body')
    