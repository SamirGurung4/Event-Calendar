from django.db import models


class Event(models.Model):
    """
    Model representing an event in the calendar.

    Attributes:
        title (str)
        start_date (Date)
        end_date (date)
        time (time, optional)
    """
    title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    time = models.TimeField(blank=True, null=True)
