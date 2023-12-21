# views.py
from django.db.models import DateTimeField, Count
from django.db.models.functions import TruncDay, TruncDate
from django.shortcuts import render
from django.views import View
from .models import Event, Reminder
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db import models
from django.db.models.functions import TruncMonth



class CalendarView(View):
    """
    View for handling initializing calendar and submitting event forms
    """

    template_name = 'calendar.html'

    def get_context_data(self, **kwargs):
        """
        :param kwargs:
            Retrieves the context data for rendering the calendar template.
        :return:
            A dictionary containing the context data, including the 'events' key with all events.
        """
        # Group events by month
        events_by_month = Event.objects.annotate(
            month=TruncMonth('start_date')
        ).values('month').annotate(event_count=Count('id')).order_by('month')

        context = {'events_by_month': events_by_month}
        return context

    def get(self, request, *args, **kwargs):
        """
        Renders the calendar template with context data.
        :param request:
            The HTTP request object.
        :param args:
            Additional positional arguments.
        :param kwargs:
            Additional keyword arguments.
        :return:
            The rendered calendar template with context data.
        """
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        """
        :param request:
            The HTTP request object.
        :param args:
            Additional positional arguments.
        :param kwargs:
            Additional keyword arguments.
        :return:
            JsonResponse: A JSON response indicating the success or failure of the data submission.
        """
        title = request.POST.get('title')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        time = request.POST.get('time')
        reminder_text = request.POST.get('reminderText')
        reminder_date = request.POST.get('reminderDate')
        reminder_time = request.POST.get('reminderTime')

        if title and start_date and end_date:
            # Create and save the event to the database
            event = Event.objects.create(
                title=title,
                start_date=start_date,
                end_date=end_date,
                time=time
            )

            # Check if reminder data is provided and create a reminder
            if reminder_text and reminder_date:
                reminder = Reminder.objects.create(
                    event=event,
                    reminder_text=reminder_text,
                    reminder_date=reminder_date,
                    reminder_time=reminder_time
                )

            return JsonResponse({'status': 'success', 'event_id': event.id})
        else:
            return JsonResponse({'status': 'error', 'message': 'Incomplete data'})


class DeleteEventView(View):
    """
    View for handling the deletion of events from the calendar.
    """

    template_name = 'calendar.html'

    def post(self, request, *args, **kwargs):
        """
        :param request:
            The HTTP request object.
        :param args:
            Additional positional arguments.
        :param kwargs:
            Additional keyword arguments.
        :return:
            JsonResponse: A JSON response indicating the success or failure of the event deletion.
        """
        event_id = request.POST.get('event_id')

        try:
            event = get_object_or_404(Event, id=event_id)
            event.delete()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})




def get_events(request):
    events = Event.objects.all()

    return {
        "events": events
    }


def dashboard_data(request):
    # Fetch chart data
    events = Event.objects.all()
    event_data = (
        events.annotate(created_at_trunc=TruncMonth('start_date'))
        .values('created_at_trunc')
        .annotate(event_count=Count('id'))
        .order_by('created_at_trunc')
        .values('created_at_trunc', 'event_count')
    )

    # Prepare data for Chart.js
    labels = [entry['created_at_trunc'].strftime('%Y-%m') for entry in event_data]
    data = [entry['event_count'] for entry in event_data]


    # Create variables for data structure that can hold the required data
    dashboard_event_chart_data = {
        'labels': labels,
        'data': data,
    }

    return {
        'dashboard_event_chart_data': dashboard_event_chart_data,
        # Add more chart data variables here if needed
    }
