import unittest
from unittest.mock import Mock
from unittest.mock import patch
import Calendar
# Add other imports here if needed


class CalendarTest(unittest.TestCase):

    # This test tests number of upcoming events.
    def test_get_upcoming_events_number(self):
        num_events = 2
        time = "2020-08-03T00:00:00.000000Z"

        mock_api = Mock()
        events = Calendar.get_upcoming_events(mock_api, time, num_events)

        self.assertEqual(mock_api.events.return_value.list.return_value.execute.return_value.get.call_count, 1)

        args, kwargs = mock_api.events.return_value.list.call_args_list[0]
        self.assertEqual(kwargs['maxResults'], num_events)


    # This tests that an error is thrown when the number of events passed is zero.
    def test_get_upcoming_events_number_zero(self):
        num_events = 0
        time = "2020-08-03T00:00:00.000000Z"

        mock_api = Mock()

        with self.assertRaises(ValueError):
            Calendar.get_upcoming_events(mock_api, time, num_events)

     # This test tests the number of past events.
    def test_get_past_events_number(self):
        num_events = 2
        time = "2020-08-03T00:00:00.000000Z"

        mock_api = Mock()
        events = Calendar.get_past_events(mock_api, time, num_events)

        self.assertEqual(mock_api.events.return_value.list.return_value.execute.return_value.get.call_count, 1)

        args, kwargs = mock_api.events.return_value.list.call_args_list[0]
        self.assertEqual(kwargs['maxResults'], num_events)

    # This tests that an error is thrown when the number of events passed is zero.
    def test_get_past_events_number_zero(self):
            num_events = 0
            time = "2020-08-03T00:00:00.000000Z"

            mock_api = Mock()

            with self.assertRaises(ValueError):
                Calendar.get_past_events(mock_api, time, num_events)       

    # Test the output in the case where no events are found in the given period
    def test_no_events_returned(self):
        events = []
        message = "No upcoming events found."

        mock_api = Mock()

        self.assertEqual(Calendar.events_output(events, mock_api), message)

    # Test the case where user has not set any reminders
    @patch('Calendar.get_default_reminders', return_value=[{'method': 'popup', 'minutes': 10}])
    def test_valid_upcoming_event_output_with_default_reminders(self, mock_get_default_reminders):
        mock_api = Mock()
        # mock_api.events.return_value.list.return_value.execute.return_value = {'method': 'popup', 'minutes': 10}
        event = {
            'summary': 'Google I/O 2015',
            'location': '800 Howard St., San Francisco, CA 94103',
            'description': 'A chance to hear more about Google\'s developer products.',
            'start': {
                'dateTime': '2015-05-28T09:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': '2015-05-28T17:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
            'recurrence': [
                'RRULE:FREQ=DAILY;COUNT=2'
            ],
            'attendees': [
                {'email': 'lpage@example.com'},
                {'email': 'sbrin@example.com'},
            ],
            'reminders': {
                'useDefault': True,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }
        self.assertEqual("Reminders for Google I/O 2015:\n"
                         " - popup 10 minutes before\n", Calendar.get_reminders(event, mock_api))

    # Test that all set reminders are returned if the event has user-set reminders
    def test_valid_upcoming_event_output_with_set_reminders(self):
        mock_api = Mock()
        event = {
            'summary': 'Google I/O 2015',
            'location': '800 Howard St., San Francisco, CA 94103',
            'description': 'A chance to hear more about Google\'s developer products.',
            'start': {
                'dateTime': '2015-05-28T09:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': '2015-05-28T17:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
            'recurrence': [
                'RRULE:FREQ=DAILY;COUNT=2'
            ],
            'attendees': [
                {'email': 'lpage@example.com'},
                {'email': 'sbrin@example.com'},
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }
        self.assertEqual("Reminders for Google I/O 2015:\n"
                         " - email 1440 minutes before\n" +
                         " - popup 10 minutes before\n", Calendar.get_reminders(event, mock_api))

    

def main():
    # Create the test suite from the cases above.
    suite = unittest.TestLoader().loadTestsFromTestCase(CalendarTest)
    # This will run the test suite.
    unittest.TextTestRunner(verbosity=2).run(suite)


main()
