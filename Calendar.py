# Make sure you are logged into your Monash student account.
# Go to: https://developers.google.com/calendar/quickstart/python
# Click on "Enable the Google Calendar API"
# Configure your OAuth client - select "Desktop app", then proceed
# Click on "Download Client Configuration" to obtain a credential.json file
# Do not share your credential.json file with anybody else, and do not commit it to your A2 git repository.
# When app is run for the first time, you will need to sign in using your Monash student account.
# Allow the "View your calendars" permission request.


# Students must have their own api key
# No test cases needed for authentication, but authentication may required for running the app very first time.
# http://googleapis.github.io/google-api-python-client/docs/dyn/calendar_v3.html


# Code adapted from https://developers.google.com/calendar/quickstart/python
from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def get_calendar_api():  # pragma: no cover
    """
    Get an object which allows you to consume the Google Calendar API.
    You do not need to worry about what this function exactly does, nor create test cases for it.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)


def get_upcoming_events(api, current_time, number_of_events):

    # Shows basic usage of the Google Calendar API.
    # Prints the start and name of the next n events on the user's calendar.

    if number_of_events <= 0:
        raise ValueError("Number of events must be at least 1.")

    events_result = api.events().list(calendarId='primary', timeMin=current_time,
                                      maxResults=number_of_events, singleEvents=True,
                                      orderBy='startTime').execute()
    return events_result.get('items', [])

    # Add your methods here.


def get_past_events(api, current_time, number_of_events):

    # Prints the start and name of the previous n events on the user's calendar.

    if number_of_events <= 0:
        raise ValueError("Number of events must be at least 1.")
    events_result = api.events().list(calendarId='primary', timeMax=current_time,
                                      maxResults=number_of_events, singleEvents=True,
                                      orderBy='startTime').execute()

    return events_result.get('items', [])


def events_output(events, api):

    #Prints the array of events that have been parsed in

    message = ""
    if not events:
        message = 'No upcoming events found.'
        return message
        # print('No upcoming events found.')

    i = 0

    for event in events:

        i += 1

        start = event['start'].get('dateTime', event['start'].get('date'))

        # Formatted the String to be more readable
        message += str(i) + ": " + start.replace("T", "  ").replace(":00+10:00", " (AEST)").replace(":00+11:00", " (AEDT)") + "  " + \
            event['summary'] + "  (Event ID: " + event['id'] + \
            ")\n" + get_reminders(event, api) + "\n"

        # print(start, event['summary'])

    return message


def get_default_reminders(api):

    # The function will print the default reminder if no custom reminder was found
    # Called whenever get_reminders cannot find any custom reminders

    events = api.events().list(calendarId='primary').execute()
    reminders = events.get('defaultReminders', [])
    return reminders


def get_reminders(event, api):

    # This function will retrieve and print any upcoming reminders for events
    # It is called whenever events_output prints an event

    reminders = []
    message = "Reminders for " + event['summary'] + ":\n"
    if event.get('reminders', []).get('useDefault') is True:

        reminders = get_default_reminders(api)

    else:
        reminders = event.get('reminders', []).get('overrides')

    for reminder in reminders:
        message += " - " + \
            reminder.get('method') + " " + \
            str(reminder.get('minutes')) + " minutes before\n"

    return message


def navigate_calendar(api, start_date, end_date):

    # Function #1 to fulfill the requirements of User Story #3
    # Retrieves the events between a given date
    # Format of the date is ISO Format (YYYY-MM-DD)

    events_result = api.events().list(calendarId='primary', timeMin=start_date, timeMax=end_date, singleEvents=True,
                                      orderBy='startTime').execute()

    return events_result.get('items', [])


def select_event_from_result(events_results, selection):

    # Function #2 to fulfill the requirements of User Story #3
    # From the retrieved events, allows the user to select their chosen event
    # Returns the chosen event to main to be parsed into other functions

    selection -= 1

    if selection > len(events_results)-1 or selection < 0:
        raise IndexError("Error: no event with number " +
                         str(int(selection+1)))

    selected_event = events_results[selection]

    return selected_event


def get_event_description(event):

    # Function #3 to fulfill the requirements of User Story #3
    # Fetches and prints the description of the event parsed into the function

    event_desc = event.get('description')

    if not event_desc:
        print("Event has no description")
    else:
        print(event_desc)


def get_searched_event(api, search_string): 

    # User Story #4
    # Allows the user to search for events via key words
    # searching for reminders yet to be implemented

    if not search_string:
        raise ValueError(
            "Search string cannot be null. Please enter a valid search string")

    search_results = api.events().list(calendarId='primary', q=search_string).execute()

    return search_results.get('items', [])


def delete_event(api, event):
    # api.events().delete(calendarId='primary', eventId=event.get('id')).execute()
    # print(event.get('summary') + " has been successfully deleted.")

    check_success = False

    try:
        api.events().delete(calendarId='primary', eventId=event.get('id')).execute()
        check_success = True
    except TypeError:
        print("No event found in API with given event ID")

    return check_success


def main():  # pragma: no cover

    print("Google Calendar\n"
          "1. See Upcoming Events\n"
          "2. See Past Events\n"
          "3. Navigate through your Calendar\n"
          "4. Search for an event\n"
          "5. Delete an Event\n")

    valid_bool_1 = False

    while not valid_bool_1:

        value = int(input("Enter a number based on the options available: "))

        api = get_calendar_api()
        time_now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

        if value == 1:
            print("\nYour upcoming events are:")
            upcoming_events = get_upcoming_events(api, time_now, 10)
            print(events_output(upcoming_events, api))
            valid_bool_1 = True

        elif value == 2:
            print("\nYour past events are:")
            past_events = get_past_events(api, time_now, 10)
            print(events_output(past_events, api))
            valid_bool_1 = True

        elif value == 3:
            print("Enter the start date & end date to search (ISO Format: YYYY-MM-DD))")

            start_date = input("Start Date: ") + "T00:00:00.000000Z"
            end_date = input("End Date: ") + "T23:59:59.000000Z"

            navigate_results = navigate_calendar(api, start_date, end_date)

            print(events_output(navigate_results, api))

            select_value = int(input("Select an event: "))

            selected_event = select_event_from_result(
                navigate_results, select_value)

            print("1. See Specific Details\n"
                  "2. Delete Event\n"
                  "3. Exit Navigation\n")

            valid_bool_2 = False

            while not valid_bool_2:
                nav_value = int(
                    input("Enter a number based on the options available: "))

                if nav_value == 1:
                    get_event_description(selected_event)
                    valid_bool_2 = True

                elif nav_value == 2:
                    delete_event(api, selected_event)
                    valid_bool_2 = True

                elif nav_value == 3:
                    print("See ya!")
                    valid_bool_2 = True
                    exit

                else:
                    print("You did not enter a valid input, please try again.")

            valid_bool_1 = True

        elif value == 4:
            keyword = input("Enter search key word: ")
            searched_events = get_searched_event(api, keyword)
            print("\n" + events_output(searched_events, api))
            valid_bool_1 = True

        elif value == 5:
            event_id = input("Enter ID of the event you want to delete: ")
            delete_event(api, event_id)
            valid_bool_1 = True

        else:
            print("You did not enter a valid input.")


if __name__ == "__main__":  # Prevents the main() function from being called by the test suite runner
    main()
