import unittest
from unittest.mock import Mock
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

    def test_no_upcoming_events(self):



    def test_get_past_events_number(self):
        num_events = 2
        time = "2020-08-03T00:00:00.000000Z"

        mock_api = Mock()
        events = Calendar.get_past_events(mock_api, time, num_events)

        self.assertEqual(mock_api.events.return_value.list.return_value.execute.return_value.get.call_count, 1)

        args, kwargs = mock_api.events.return_value.list.call_args_list[0]
        self.assertEqual(kwargs['maxResults'], num_events)


def main():
    # Create the test suite from the cases above.
    suite = unittest.TestLoader().loadTestsFromTestCase(CalendarTest)
    # This will run the test suite.
    unittest.TextTestRunner(verbosity=2).run(suite)


main()
