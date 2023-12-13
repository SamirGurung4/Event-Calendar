from django.shortcuts import render
from django.views import View
from .models import Event
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


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
        context = {}
        context['events'] = Event.objects.all()
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

        if title and start_date and end_date:
            # Create and save the event to the database
            Event.objects.create(
                title=title,
                start_date=start_date,
                end_date=end_date,
                time=time
            )

            return JsonResponse({'status': 'success'})
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

