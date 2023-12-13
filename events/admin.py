from django.contrib import admin
from .models import Event


class EventAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Event model.
    """
    list_display = ('title', 'start_date', 'end_date', 'time')
    search_fields = ['title']


admin.site.register(Event, EventAdmin)
