# admin.py
from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from .models import Event, Reminder


class ReminderInline(admin.TabularInline):
    model = Reminder
    extra = 1


class CustomChangeList(ChangeList):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


@admin.register(Event)
class CustomEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'time')
    search_fields = ['title', 'start_date', 'end_date']
    ordering = ['start_date']
    inlines = [ReminderInline]

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        return response

    def get_changelist(self, request, **kwargs):
        return CustomChangeList


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('reminder_text', 'event', 'reminder_date', 'reminder_time')
    search_fields = ['event__title', 'reminder_text']
    list_filter = ('reminder_date',)
    ordering = ('reminder_date', 'reminder_time')
