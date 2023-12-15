from django.contrib import admin
from .models import Event, Reminder


class ReminderInline(admin.TabularInline):
    model = Reminder
    extra = 1


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Event model.
    """
    list_display = ('title', 'start_date', 'end_date', 'time')
    search_fields = ['title']
    ordering = ['start_date']
    inlines = [ReminderInline]

    fieldsets = (
        ('Event Details', {
            'fields': ('title', 'start_date', 'end_date', 'time'),
        }),
    )


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Reminder model.
    """
    list_display = ('reminder_text', 'event', 'reminder_date', 'reminder_time')
    search_fields = ['event__title', 'reminder_text']
    list_filter = ('reminder_date',)
    ordering = ('reminder_date', 'reminder_time')
