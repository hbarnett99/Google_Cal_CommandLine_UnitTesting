# Test Strategy
## FIT2107-S2-2020 Assignment 2
### Henry Barnett & Daniel Low


# [Check here for a Sytax guide to writing Markdown file](https://www.markdownguide.org/basic-syntax/)

### Current [Lucid chart](https://app.lucidchart.com/invitations/accept/5c0e83f4-3b4b-4e0e-90d2-eb00f4e7fe7f) for program CFG

CFGs were chosen to base test cases on as functions rarely had multiple conditions, making an MC/DC table feel redunant. An MC/DC table also does not show a function's loop as well as a CFG does, making a CFG the ideal methodology to plan our tests around.

A lot of the function's CFGs look the same as they are all built very similarly, first checking for an error to be raised. Example

## Function Example
        def get_searched_event(api, search_string):
        if not search_string:
            raise ValueError("Search string cannot be null. Please enter a valid search string")

        search_results = api.events().list(calendarId='primary', q=search_string).execute()

        return search_results.get('items', [])`

From this, fairly uniform tests can be built, and are likely to only require two tests each. One to see if it behaves as expected with a correct variable parsed in, and another with an invalid variable to see if the raised error is reached. 

For coverage reporting, ___main():___ and ___get_calendar_api():___ have been ignored with the following comment, which can be found next to each of the above functions.

    # pragma: no cover