from libevent.dal import EventDal
import json
import datetime


class EventBl:
    """A business logic layer: Used to add event, rules to event, execute event & get event data."""

    event_rule_keys = ["event_rule_name", "event_rule_no_of_attempts", "event_rule_time_interval"]

    def __init__(cls):
        pass

    @classmethod
    def add_event(cls, event_noun, event_verb, event_data, custom_event=False):
        """
        Creates a new event

        :param event_noun: Name of the event [String, Required]
        :param event_verb: Name of the event verb [String, Required]
        :param event_data: Data associated with event [String, Optional]
        :param custom_event: True, when event is created after rule is triggered [Boolean, Optional]
        :return: void
        """

        event_id = EventDal.get_event_id_from_noun_verb(event_noun, event_verb)
        if event_id < 0:
            event_id = EventDal.add_event(event_noun, event_verb, custom_event)

        EventBl.__add_event_data(event_id, event_data)

        if custom_event is False:
            EventBl.__trigger_rule_check(event_id, event_verb, event_rule_id=None)

    @classmethod
    def add_rule_to_event(cls, event_rule, event_noun, event_verb):
        """
        Adds rule to the existing event

        :param event_rule: A dictionary object with required values. [Dictionary, Required]
                    event_rule_name: Name of the event rule. Eg., "login-failed" [String]
                    event_rule_no_of_attempts: Number of attempts or calls made to the specific event which helps to
                                               determine when to save event data with event_rule_time_interval key[Integer]
                    event_rule_time_interval: Time interval in minutes. [Integer]
        :param event_noun: Name of the existing event name. [String, Required]
        :param event_verb: Name of the existing event verb. Eg., "failed" [String, Optional]
        :return: void
        """

        if EventBl.__check_if_event_exist(event_noun, event_verb):
            for key in cls.event_rule_keys:
                if key in event_rule:
                    print("EventBl | add_rule_to_event '{}'| The value of {} is {}".format(event_noun, key, event_rule[key]))
                else:
                    raise ValueError("Please provide value for %s" % key)
        else:
            print("EventBl | add_rule_to_event | Event %s not found in db | Please provide valid event" % event_noun)

        if EventDal.is_event_rule_in_db(event_rule["event_rule_name"]) is not True:
            event_noun_id, event_rule_id = EventDal.add_rule_to_event(event_rule, event_noun, event_verb)
            EventBl.__trigger_rule_check(event_noun_id, event_verb, event_rule_id)


    @staticmethod
    def __add_event_data(event_id, event_data):
        """
        Add event data
        :param event_id: Event Id of the event [Integer, Required]
        :param event_id: Data associated with the event [String, Required]
        :return: void
        """
        print("EventBl | __add_event_data | Add event data")
        event_noun_info = EventDal.get_event_info_from_id(event_id)
        EventBl.__store_json_data(event_noun_info, event_data)

    @staticmethod
    def get_event_data(page_number, no_of_items_per_page, event_noun=None, event_verb=None):
        if event_noun is not None:
            return EventDal.get_event_data(page_number, no_of_items_per_page, event_noun=event_noun)
        elif event_verb is not None:
            return EventDal.get_event_data(page_number, no_of_items_per_page, event_noun=event_noun, event_verb=event_verb)
        else:
            return EventDal.get_event_data(page_number, no_of_items_per_page)


    @staticmethod
    def __trigger_rule_check(event_noun_id, event_verb, event_rule_id=None):
        """
        It check's no of successive calls made to a particular event within a time interval.
        Store json if event rules are met.
        :param event_noun_id: Event Id [Integer, Required]
        :param event_verb: Verb of the event [String, Required]
        :param event_rule_id: Rule Id of the event [Integer, Optional]
        :return: void
        """
        if event_rule_id is None:
            event_rule_id = EventDal.get_event_rule_id_from_noun_id(event_noun_id)
            if event_rule_id < 0:
                return

        no_of_successive_calls = EventBl.__get_no_of_eventcalls_within_time_interval(event_noun_id, event_rule_id)
        event_rule_info = EventDal.get_event_rule_info(event_rule_id)

        if no_of_successive_calls >= event_rule_info["event_rule_no_of_attempts"]:
            custom_event_name = "{}-{}".format(event_rule_info["event_rule_name"],"alert")
            print ("Rule satisfied, creating custom event %s" % custom_event_name)

            custom_event_data = {}
            custom_event_data["rule-statement"] = "This event/verb has been called for {} times within {} minutes".format(no_of_successive_calls, event_rule_info["event_rule_time_interval"])

            EventBl.add_event(custom_event_name, event_verb, custom_event_data, custom_event=True)

    @staticmethod
    def __check_if_event_exist(event_noun, event_verb):
        return EventDal.get_event_id_from_noun_verb(event_noun, event_verb)

    @staticmethod
    def __get_no_of_eventcalls_within_time_interval(event_noun_id, event_rule_id):
        return EventDal.get_no_of_eventcalls_within_time_interval(event_noun_id, event_rule_id)

    @staticmethod
    def __store_json_data(event_noun_info, event_data):
        """
        Create and store a event json object
        :param event_noun_info: A list containing event noun information [List, Required]
        :param event_data: Data associated with the event
        :return: void
        """
        jsonrep = {}
        jsonrep["noun"] = event_noun_info["event_noun"]
        jsonrep["verb"] = event_noun_info["event_verb"]
        jsonrep["timestamp"] = int(datetime.datetime.now().timestamp())
        jsonrep["data"] = [event_data]
        EventDal.add_event_data(event_noun_info["event_id"], json.dumps(jsonrep))
