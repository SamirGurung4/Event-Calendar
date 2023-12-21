# events/urls.py
from django.urls import path
from .views import CalendarView, DeleteEventView

urlpatterns = [
    path('calendar/', CalendarView.as_view(), name='calendar'),
    path('delete_event/', DeleteEventView.as_view(), name='delete_event'),
]
