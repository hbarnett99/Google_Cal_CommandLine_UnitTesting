# Test Strategy
## FIT2107-S2-2020 Assignment 2 - Henry Barnett & Daniel Low

<br>

## Test Case Methods

CFGs were chosen to base test cases on as functions rarely had multiple conditions, making an MC/DC table feel redunant. An MC/DC table also does not show a function's loop as well as a CFG does, making a CFG the ideal methodology to plan our tests around.

<br>

***Current [Lucid chart](https://app.lucidchart.com/invitations/accept/5c0e83f4-3b4b-4e0e-90d2-eb00f4e7fe7f) for program CFG*** 

##### *Theres also a [PDF](https://drive.google.com/file/d/1d9Q-yeQ8WhuQNZOvgoGjPw7NLvevt_YT/view?usp=sharing) if that is easier*

<br>

Functions should be built to test each possible path the program can take as per the CFG, giving complete statement coverage, as well as branch coverage.

A lot of the function's CFGs look the same as they are all built very similarly, first checking for an error to be raised, and then processing the fucntion required in a single line or so.

## Function Example
    def get_searched_event(api, search_string):
        if not search_string:
            raise ValueError("Search string cannot be null. Please enter a valid search string")

        search_results = api.events().list(calendarId='primary', q=search_string).execute()

        return search_results.get('items', [])`

From this, fairly uniform tests can be built, and are likely to only require two tests each. One to see if it behaves as expected with a correct variable parsed in, and another with an invalid variable to see if the raised error is reached. 

Test cases should also somewhat cover the elements that have been taken to handle as many exceptions that may normally be found in blackbox testing (eg. out of bounds of conditions).

<br>

## Mocking

Mocking is used to simulate the use of the Google Calendar API, without having to work on a live information, which can be especially dangerous when modifying and deleting events. It also becomes extremely useful, allowing us to see what is expected from each of the functions created.

The mock API allows us to test functions in isolation, which makes it quick, clear and concise when finding what is and is not working when testing the functions in isolation.

<br>

 ## How Much Coverage?

For coverage reporting, ___main():___ and ___get_calendar_api():___ will be ignored with the following comment, which can be found next to each of the above functions. 

    # pragma: no cover

As per Najam, any logic regarding UI or program interface is not required. This is all kept in ___main():___. 

For ___get_calendar_api():___, the function, it was included in the original code provided to us, and therefore is not required to be tested.

Having ignored these, the aim is that the test suites should reach 100% coverage. At 100%, there is both complete branch coverage, giving strong confidence in the program to behave as expected. 

<br>

 ## Coverage Report
 ![Coverage](https://i.ibb.co/MZH992P/121371216-765769820822104-3375311843424163557-n.png)

<br>

# Test Suites
**Tests should match the following, and no more to ensure that a minimum amount of test cases are required, while still achieving 100% statement coverage.** *However, they may be a little scrambled in their arrangement within the test code*

## Miscellaneous Suite
### Function: events_output
- Test #1 - Test with no events returned
- Test #2 - Test with events returned
### Function: get_event_description
- Test #3 - Test event with description
- Test #4 - Test event with no description
### Function: get_reminders
- Test #3 - Test event with default reminders
- Test #4 - Test event with additional (multiple) reminders

<br>

## Suite 1 - User Story #1
### Function: get_past_events
- Test #1 - Test with valid number of events
- Test #2 - Test with no past events

<br>

## Suite 2 - User Story #2
### Function: upcoming_events
- Test #1 - Test with valid number of events
- Test #2 - Test with no past events

<br>

## Suite 3 - User Story #3
### Function: navigate_calendar
- Test #1 - Test with valid start date and end date
- Test #2 - Test with no valid dates, but invalid start date and end date
### Function: select_event_from_result
- Test #1 - Test with valid number to select event
- Test #2 - Test with number out of bounds of the event list

<br>

## Suite 4 - User Story #4
### Function: get_searched_event
- Test #1 - Test with a valid search query
- Test #2 - Test with an empty search query

<br>

## Suite 5 - User Story #5
### Function: delete_event
- Test #1 - Test with an event to delete
- *note that no other tests were completed for this, as the way the code is written a valid event is found, therefore the user cannot parse an event that does not exist within the API*
