from django.test import TestCase
from events.models import Event, Reminder
from datetime import date, time


class EventModelTest(TestCase):
    def test_event_creation(self):
        # Create an Event instance
        event = Event.objects.create(
            title='Test Event',
            start_date=date(2023, 1, 1),
            end_date=date(2023, 1, 2),
            time=time(12, 0),
        )

        # Retrieve the created event from the database
        created_event = Event.objects.get(id=event.id)

        # Check if the created event matches the expected data
        self.assertEqual(created_event.title, 'Test Event')
        self.assertEqual(created_event.start_date, date(2023, 1, 1))
        self.assertEqual(created_event.end_date, date(2023, 1, 2))
        self.assertEqual(created_event.time, time(12, 0))

    def test_event_str_method(self):
        # Create an Event instance
        event = Event.objects.create(
            title='Another Event',
            start_date=date(2023, 2, 1),
            end_date=date(2023, 2, 2),
            time=time(15, 30),
        )

        # Check if the __str__ method returns the expected string
        self.assertEqual(str(event), 'Another Event')

class ReminderModelTest(TestCase):
    def test_reminder_creation(self):
        # Create an Event instance for associating with the Reminder
        event = Event.objects.create(
            title='Test Event',
            start_date=date(2023, 1, 1),
            end_date=date(2023, 1, 2),
            time=time(12, 0),
        )

        # Create a Reminder instance
        reminder = Reminder.objects.create(
            event=event,
            reminder_text='Test Reminder',
            reminder_date=date(2023, 1, 1),
            reminder_time=time(10, 0),
        )

        # Retrieve the created reminder from the database
        created_reminder = Reminder.objects.get(id=reminder.id)

        # Check if the created reminder matches the expected data
        self.assertEqual(created_reminder.event, event)
        self.assertEqual(created_reminder.reminder_text, 'Test Reminder')
        self.assertEqual(created_reminder.reminder_date, date(2023, 1, 1))
        self.assertEqual(created_reminder.reminder_time, time(10, 0))

    def test_reminder_str_method(self):
        # Create an Event instance for associating with the Reminder
        event = Event.objects.create(
            title='Yet Another Event',
            start_date=date(2023, 3, 1),
            end_date=date(2023, 3, 2),
            time=time(18, 0),
        )

        # Create a Reminder instance
        reminder = Reminder.objects.create(
            event=event,
            reminder_text='Another Reminder',
            reminder_date=date(2023, 3, 1),
            reminder_time=time(16, 0),
        )

        # Check if the __str__ method returns the expected string
        self.assertEqual(str(reminder), 'Yet Another Event - Another Reminder')
