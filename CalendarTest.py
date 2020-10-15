import unittest
from unittest.mock import Mock
from unittest.mock import patch
import Calendar
# Add other imports here if needed


class Miscellaneous_CalendarTest(unittest.TestCase):

    # Test the output in the case where no events are found in the given period
    def test_no_events_returned(self):
        events = []
        message = "No upcoming events found."

        mock_api = Mock()

        self.assertEqual(Calendar.events_output(events, mock_api), message)


    # This test tests the return of reminders when the default reminder is used
    @patch('Calendar.get_default_reminders', return_value=[{'method': 'popup', 'minutes': 10}])
    def test_get_reminders_when_default_is_true(self, mock_get_default_reminders):
        mock_api = Mock()
        event = {
            'summary': 'Test Event 1',
            'id': '12345',
            'start': {
                'dateTime': '2015-05-28T09:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': '2015-05-28T17:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
            'reminders': {
                'useDefault': True,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }

        message = "Reminders for Test Event 1:\n"\
                    " - popup 10 minutes before\n"
        self.assertEqual(Calendar.get_reminders(event, mock_api), message)  

    # This test tests the return of reminders when user set reminders are used
    def test_get_reminders_when_default_is_false(self):
        mock_api = Mock()
        event = {
            'summary': 'Test Event 1',
            'id': '12345',
            'start': {
                'dateTime': '2015-05-28T09:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': '2015-05-28T17:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }

        message = "Reminders for Test Event 1:\n"\
                    " - email 1440 minutes before\n"\
                    " - popup 10 minutes before\n"
        self.assertEqual(Calendar.get_reminders(event, mock_api), message)  


    @patch('Calendar.get_reminders', return_value=' - popup 10 mins before')
    def test_events_output_format(self, mock_get_reminders):
        mock_api = Mock();

        events = [{
            'summary': 'Test Event 1',
            'id': '12345',
            'start': {
                'dateTime': '2015-05-28T09:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': '2015-05-28T17:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
            'reminders': {
                'useDefault': True,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }, {
            'summary': 'Test Event 2',
            'id': '23456',
            'start': {
                'dateTime': '2015-05-28T09:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': '2015-05-28T17:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
            'reminders': {
                'useDefault': True,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }]

        message = "1: 2015-05-28  09:00:00-07:00  Test Event 1  (Event ID: 12345)\n"\
                      " - popup 10 mins before\n"\
                      "2: 2015-05-28  09:00:00-07:00  Test Event 2  (Event ID: 23456)\n"\
                      " - popup 10 mins before\n"
        self.assertEqual(Calendar.events_output(events, mock_api), message)

class UserStory1_CalendarTest(unittest.TestCase):

    # This test tests the number of past events.
    def test_get_past_events_number(self):
        num_events = 2
        time = "2020-08-03T00:00:00.000000Z"

        mock_api = Mock()
        events = Calendar.get_past_events(mock_api, time, num_events)

        self.assertEqual(
            mock_api.events.return_value.list.return_value.execute.return_value.get.call_count, 1)

        args, kwargs = mock_api.events.return_value.list.call_args_list[0]
        self.assertEqual(kwargs['maxResults'], num_events)

    # This tests that an error is thrown when the number of events passed is zero.
    def test_get_past_events_number_zero(self):
        num_events = 0
        time = "2020-08-03T00:00:00.000000Z"

        mock_api = Mock()

        with self.assertRaises(ValueError):
            Calendar.get_past_events(mock_api, time, num_events)

class UserStory2_CalendarTest(unittest.TestCase):

    # This test tests number of upcoming events.
    def test_get_upcoming_events_number(self):
        num_events = 2
        time = "2020-08-03T00:00:00.000000Z"

        mock_api = Mock()
        events = Calendar.get_upcoming_events(mock_api, time, num_events)

        self.assertEqual(
            mock_api.events.return_value.list.return_value.execute.return_value.get.call_count, 1)

        args, kwargs = mock_api.events.return_value.list.call_args_list[0]
        self.assertEqual(kwargs['maxResults'], num_events)

    # This tests that an error is thrown when the number of events passed is zero.
    def test_get_upcoming_events_number_zero(self):
        num_events = 0
        time = "2020-08-03T00:00:00.000000Z"

        mock_api = Mock()

        with self.assertRaises(ValueError):
            Calendar.get_upcoming_events(mock_api, time, num_events)

    # Test the case where user has not set any reminders
    @patch('Calendar.get_default_reminders', return_value=[{'method': 'popup', 'minutes': 10}])
    def test_valid_upcoming_event_output_with_default_reminders(self, mock_get_default_reminders):
        mock_api = Mock()
        # mock_api.events.return_value.list.return_value.execute.return_value = {'method': 'popup', 'minutes': 10}
        event = {
            'summary': 'Google I/O 2015',
            'start': {
                'dateTime': '2015-05-28T09:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': '2015-05-28T17:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
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
            'start': {
                'dateTime': '2015-05-28T09:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': '2015-05-28T17:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
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

class UserStory3_CalendarTest(unittest.TestCase):
    #The following tests test User Story #3 - Navigate calendar

    def test_navigate_calendar_valid(self):
        start_date = "2020-10-10T00:00:00.000000Z"
        end_date = "2020-11-11T23:59:59.000000Z"

        mock_api = Mock()

        events = Calendar.navigate_calendar(mock_api, start_date, end_date)

        self.assertEqual(
            mock_api.events.return_value.list.return_value.execute.return_value.get.call_count, 1)

        args, kwargs = mock_api.events.return_value.list.call_args_list[0]
        self.assertEqual(kwargs['timeMin'], start_date)
        self.assertEqual(kwargs['timeMax'], end_date)

    def test_select_event_from_result(self):

        event_1 = {
            'summary': 'Test Event 1',
            'id': '12345',
            'start': {
                'dateTime': '2015-05-28T09:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': '2015-05-28T17:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
            'reminders': {
                'useDefault': True,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }

        event_2 = {
            'summary': 'Test Event 2',
            'id': '23456',
            'start': {
                'dateTime': '2015-05-28T09:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': '2015-05-28T17:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
            'reminders': {
                'useDefault': True,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }

        event_list = [event_1, event_2]
        selection_number = 2
        mock_api = Mock()

        self.assertEqual(Calendar.select_event_from_result(
            event_list, selection_number), event_2)

    def test_select_event_from_result_invalid_number(self):

        event_1 = {
            'summary': 'Test Event 1',
            'id': '12345',
            'start': {
                'dateTime': '2015-05-28T09:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': '2015-05-28T17:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
            'reminders': {
                'useDefault': True,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }

        event_2 = {
            'summary': 'Test Event 2',
            'id': '23456',
            'start': {
                'dateTime': '2015-05-28T09:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': '2015-05-28T17:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
            'reminders': {
                'useDefault': True,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }

        event_list = [event_1, event_2]
        selection_number = 200
        message = "Error: no event with number " + str(int(selection_number+1))

        with self.assertRaises(IndexError):
            (Calendar.select_event_from_result(
                event_list, selection_number), message)

class UserStory4_CalendarTest(unittest.TestCase):

            #The following tests test User Story #4 - Search events

            # @patch('Calendar.get_searched_event', return_value=[{"Example"}])
        def test_get_searched_event_with_query(self):
            query = "Search Query"
            mock_api = Mock()

            events = Calendar.get_searched_event(mock_api, query)

            self.assertEqual(
                mock_api.events.return_value.list.return_value.execute.return_value.get.call_count, 1)

            args, kwargs = mock_api.events.return_value.list.call_args_list[0]
            self.assertEqual(kwargs['q'], query)

        def test_get_searched_event_with_empty_query(self):
            query = ""
            mock_api = Mock()

            message = "Search string cannot be null. Please enter a valid search string"

            with self.assertRaises(ValueError):
                (Calendar.get_searched_event(mock_api, query), message)


class UserStory5_CalendarTest(unittest.TestCase):
    print("Yet to implement tests for User Story #5")

def main():
    # Create the test suite from the cases above.
    suitemisc = unittest.TestLoader().loadTestsFromTestCase(Miscellaneous_CalendarTest)
    suite1 = unittest.TestLoader().loadTestsFromTestCase(UserStory1_CalendarTest)
    suite2 = unittest.TestLoader().loadTestsFromTestCase(UserStory2_CalendarTest)
    suite3 = unittest.TestLoader().loadTestsFromTestCase(UserStory3_CalendarTest)
    suite4 = unittest.TestLoader().loadTestsFromTestCase(UserStory4_CalendarTest)
    suite5 = unittest.TestLoader().loadTestsFromTestCase(UserStory5_CalendarTest)


    # This will run the test suite.
    print("\nMiscellaneous Suite")
    unittest.TextTestRunner(verbosity=2).run(suitemisc)
    print("\nSuite 1 - User Story 1")
    unittest.TextTestRunner(verbosity=2).run(suite1)
    print("\nSuite 2 - User Story 2")
    unittest.TextTestRunner(verbosity=2).run(suite2)
    print("\nSuite 3 - User Story 3")
    unittest.TextTestRunner(verbosity=2).run(suite3)
    print("\nSuite 4 - User Story 4")
    unittest.TextTestRunner(verbosity=2).run(suite4)
    print("\nSuite 5 - User Story 5")
    unittest.TextTestRunner(verbosity=2).run(suite5)


main()
