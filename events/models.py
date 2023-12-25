"""
#model.py
"""
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

    def __str__(self):
        return str(self.title)


class Reminder(models.Model):
    """
    Model representing a reminder associated with an event.

    Attributes:
        event (ForeignKey)
        reminder_text (TextField)
        reminder_date (Date)
        reminder_time (Time, optional)
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    reminder_text = models.TextField()
    reminder_date = models.DateField()
    reminder_time = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.event.title} - {self.reminder_text}"



    