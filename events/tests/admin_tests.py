from django.test import TestCase, Client
from django.urls import reverse
from events.models import Event, Reminder
from django.contrib.auth.models import User


class AdminTest(TestCase):
    def setUp(self):
        # Create a superuser for logging into the admin
        self.user = User.objects.create_superuser(
            username='admin', password='admin@123', email='admin@gmail.com')
        self.client = Client()
        self.client.login(username='admin', password='admin@123')

    def test_event_admin(self):
        # Create an Event instance for testing
        event = Event.objects.create(
            title='Test Event',
            start_date='2023-01-01',
            end_date='2023-01-02',
            time='12:00',
        )

        # Test Event list view
        response = self.client.get(reverse('admin:events_event_changelist'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Event')

        # Test Event change view
        response = self.client.get(
            reverse('admin:events_event_change', args=[event.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Event')

    def test_reminder_admin(self):
        # Create an Event instance for associating with the Reminder
        event = Event.objects.create(
            title='Test Event',
            start_date='2023-01-01',
            end_date='2023-01-02',
            time='12:00',
        )

        # Create a Reminder instance for testing
        reminder = Reminder.objects.create(
            reminder_text='Test Reminder',
            event=event,
            reminder_date='2023-01-01',
            reminder_time='10:00',
        )

        # Test Reminder list view
        response = self.client.get(reverse('admin:events_reminder_changelist'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Reminder')

        # Test Reminder change view
        response = self.client.get(
            reverse('admin:events_reminder_change', args=[reminder.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Reminder')
