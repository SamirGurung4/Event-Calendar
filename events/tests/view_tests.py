from datetime import datetime, timedelta
from django.test import TestCase
from django.urls import reverse
from events.models import Event


class CalendarViewTest(TestCase):
    NUMBER_OF_DATA = 1000

    def test_event_creation_on_selecting_date(self):
        # Placeholder values for test data
        titles = ['Test Event ' + str(i) for i in range(1, self.NUMBER_OF_DATA)]
        start_dates = [(datetime(2023, 2, 1) + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, self.NUMBER_OF_DATA)]
        end_dates = [(datetime(2023, 1, 2) + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, self.NUMBER_OF_DATA)]
        times = [(datetime(1, 1, 1, 0, 0) + timedelta(hours=i)).strftime('%H:%M:%S') for i in range(1, self.NUMBER_OF_DATA)]
        reminder_texts = ['Reminder 1'+ str(i) for i in range(1, self.NUMBER_OF_DATA)]
        reminder_dates = [(datetime(2023, 1, 1) + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, self.NUMBER_OF_DATA)]
        reminder_times = [(datetime(1, 1, 1, 0, 0, 0) + timedelta(hours=i)).strftime('%H:%M:%S') for i in range(1, self.NUMBER_OF_DATA)]

        event_data_list = [
            {
                'title': title,
                'start_date': start_date,
                'end_date': end_date,
                'time': time,
                'reminderText': reminder_text,
                'reminderDate': reminder_date,
                'reminderTime': reminder_time,
            }
            for title, start_date, end_date, time, reminder_text, reminder_date, reminder_time
            in zip(titles, start_dates, end_dates, times, reminder_texts, reminder_dates, reminder_times)
        ]

        # Loop through the list and use the event data to create events
        responses = []
        for event_data in event_data_list:
            response = self.client.post(reverse('calendar'), data=event_data)
            responses.append(response)

        # Check if all responses indicate success
        for i, response in enumerate(responses):
            self.assertEqual(response.status_code, 200, f"Response {i+1} status code: {response.status_code}")
            self.assertEqual(response.json()['status'], 'success', f"Response {i+1} status: {response.json()['status']}")

        # Check the count of events for each title
        event_count_1 = Event.objects.filter(title='Test Event').count()
        event_count_2 = Event.objects.filter(title='Test Event 2').count()
        event_count_3 = Event.objects.filter(title='Test Event 3').count()

        print(f"Event count for 'Test Event': {event_count_1}")
        print(f"Event count for 'Test Event 2': {event_count_2}")
        print(f"Event count for 'Test Event 3': {event_count_3}")

        # Assert the count of events for each title
        self.assertEqual(event_count_1, 0)
        self.assertEqual(event_count_2, 1)
        self.assertEqual(event_count_3, 1)

        # Run the previous test cases for event creation with and without time, and incomplete data
        self.test_event_creation_with_time()
        self.test_event_creation_without_time()
        self.test_event_creation_incomplete_data()

    def test_event_creation_with_time(self):
        # Define data for event creation with time
        data = {
            'title': 'Test Event',
            'start_date': '2023-01-01',
            'end_date': '2023-01-02',
            'time': '12:00:00',
            'reminderText': 'Test Reminder',
            'reminderDate': '2023-01-01',
            'reminderTime': '10:00:00',
        }

        # Make a POST request to the CalendarView endpoint
        response = self.client.post(reverse('calendar'), data)

        # Check if the response indicates success and an event ID is returned
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertTrue('event_id' in response.json())

        # Check if the event is created in the database
        event_id = response.json()['event_id']
        self.assertTrue(Event.objects.filter(id=event_id).exists())

    def test_event_creation_without_time(self):
        # Define data for event creation without time
        data = {
            'title': 'Test Event',
            'start_date': '2023-01-01',
            'end_date': '2023-01-02',
            'reminderText': 'Test Reminder',
            'reminderDate': '2023-01-01',
            'reminderTime': '10:00:00',
        }

        # Make a POST request to the CalendarView endpoint
        response = self.client.post(reverse('calendar'), data)

        # Check if the response indicates success and an event ID is returned
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertTrue('event_id' in response.json())

        # Check if the event is created in the database
        event_id = response.json()['event_id']
        self.assertTrue(Event.objects.filter(id=event_id).exists())

    def test_event_creation_incomplete_data(self):
        # Define data with incomplete information
        data = {
            'title': 'Test Event',
            'start_date': '2023-01-01',
            'reminderText': 'Test Reminder',
            'reminderDate': '2023-01-01',
            'reminderTime': '10:00:00',
        }

        # Make a POST request to the CalendarView endpoint
        response = self.client.post(reverse('calendar'), data)

        # Check if the response indicates an error due to incomplete data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'error')
        self.assertEqual(response.json()['message'], 'Incomplete data')

    def test_reminder_creation_incomplete_data(self):
        # Define data with incomplete information (missing 'reminderTime')
        data = {
            'title': 'Test Event',
            'start_date': '2023-01-01',
            'end_date': '2023-01-02',
            'reminderText': 'Test Reminder',
            'reminderDate': '2023-01-01',
        }

        # POST request to the CalendarView endpoint
        response = self.client.post(reverse('calendar'), data)

        # Check if the response indicates an error due to incomplete data
        self.assertEqual(response.status_code, 200)
        print(response.json().get('status'), "status here")
        # Check if the status is 'error' (not 'success')
        self.assertEqual(response.json().get('status'), 'error', f"Actual status: {response.json().get('status')}")

        # Check if the error message mentions the missing 'reminderTime'
        self.assertTrue('reminderTime' in response.json().get('errors', {}))

class DeleteEventViewTest(TestCase):
    def setUp(self):
        # Create a test event
        self.test_event = Event.objects.create(
            title='Test Event',
            start_date='2023-01-01',
            end_date='2023-01-02',
            time='12:00:00'
        )

    def test_event_deletion(self):
        # Make a POST request to the DeleteEventView endpoint
        response = self.client.post(reverse('delete_event'), {'event_id': self.test_event.id})

        # Check if the response indicates success
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')

        # Check if the event is deleted in the database
        self.assertFalse(Event.objects.filter(id=self.test_event.id).exists())

    def test_event_deletion_nonexistent_event(self):
        # Make a POST request to the DeleteEventView endpoint with a non-existent event ID
        response = self.client.post(reverse('delete_event'), {'event_id': 9999})

        # Check if the response indicates an error
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'error')

        # Check if the event is not deleted in the database (should still exist)
        self.assertTrue(Event.objects.filter(id=self.test_event.id).exists())

    def test_event_deletion_missing_event_id(self):
        # Make a POST request to the DeleteEventView endpoint without providing event_id
        response = self.client.post(reverse('delete_event'), {})

        # Check if the response indicates an error
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'error')

        # Check if the event is not deleted in the database (should still exist)
        self.assertTrue(Event.objects.filter(id=self.test_event.id).exists())

