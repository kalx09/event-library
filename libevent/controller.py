from libevent.bl import EventBl


class EventController:
    """
    :title:
        Event library
    :description:
        This is public interface of the event library. Validates user input before forwarding the request.
    """

    def __init__(self):
        pass

    def create_event(self, event_noun):
        """
        Creates a new event

        :param event_noun: Name of the event [String, Optional]
        :return: void
        :except: ValueError
        """

        if event_noun is None:
            raise ValueError("Please provide name of the event")
        else:
            EventBl.add_event(event_noun)

    def add_rule_to_event(self, event_rule, event_noun=None):
        """
        Adds rule to the existing event

        :param event_rule: A dictionary object with required values. [Dictionary, required]
                    event_rule_name: Name of the event rule. Eg., "login-failed" [String]
                    event_rule_verb: Name of the event verb. Eg., "failed" [String]
                    event_rule_no_of_attempts: Number of attempts or calls made to the specific event which helps to
                                               determine when to save event data with event_rule_time_interval key[Integer]
                    event_rule_time_interval: Time interval in minutes. [Integer]
        :param event_noun: Name of the existing event name. [String, required]
        :return: void
        :except: ValueError
        """

        if event_noun is None:
            raise ValueError("Please provide name of the event for which the rule is to be added")
        else:
            EventBl.add_rule_to_event(event_rule, event_noun)

    def execute_event_rule(self, event_rule_name=None, event_rule_verb=None):
        """
        Execute the event with the associated rule
        :param event_rule_name: Name of the event rule [String, required]
        :param event_rule_verb: Name of the event verb [String, required]
        :return: void
        :except: ValueError
        """
        if event_rule_name is None or event_rule_verb is None:
            raise ValueError("Please provide valid details to execute event")
        else:
            EventBl.execute_event_rule(event_rule_name, event_rule_verb)

    def get_event_data(self, event_noun=None, event_rule_name=None, event_rule_verb=None, page_number=1, no_of_items_per_page=5):
        """
        Retrieves event data. It can filer data with respect to event noun, rule name & verb.
        :param event_noun: Name of the event to get data for. Filtering with respect to event_noun [String, Optional]
        :param event_rule_name: Name of the event rule to get data for. This is mandatory if event_rule_verb is specified [String, Optional]
        :param event_rule_verb: Name of the event verb. Filtering with respect to event_verb [String, Optional]
        :param page_number: Indicates page number to be fetched [Integer, Optional]
        :param no_of_items_per_page: Number of items to retrieve on each page [Integer, Optional]
        :return: A list of event data object [Array of objects]
                eventId: Event rule name [String]
                noun: Event name [String]
                verb: Event verb name [String]
                timestamp: Epoch time when the event was recorded [Integer]
                data: Event specific data [Array]
        :except: ValueError
        """

        # Convert to int, if default value is not used
        page_num = int(page_number)
        if page_num < 1:
            raise ValueError("EventController | get_event_data | input parameter 'page_number' must be greater than 0")

        # Convert to int, if default value is not used
        items_per_page = int(no_of_items_per_page)
        if items_per_page < 1:
            raise ValueError("EventController | get_event_data | input parameter 'no_of_items_per_page' must be greater than 0")

        if event_noun is not None: # filtering on the basis of event_noun
            return EventBl.get_event_data(page_num, items_per_page, event_noun=event_noun)

        elif event_rule_verb is not None and event_rule_name is None: # filter on the basis of event_rule_verb
            raise ValueError("EventController | get_event_data | input parameter 'event_rule_name' must be "
                             "specified for event_rule_verb to be filtered")
        elif event_rule_verb is not None and event_rule_name is not None:  # filter on the basis of event_rule_verb
            return EventBl.get_event_data(page_num, items_per_page, event_rule_name=event_rule_name,
                                   event_rule_verb=event_rule_verb)
        else:
            return EventBl.get_event_data(page_num, items_per_page)
