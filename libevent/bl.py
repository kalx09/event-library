from libevent.dal import EventDal
import json
import datetime


class EventBl:
    """A business logic layer: Used to add event, rules to event, execute event & get event data."""

    event_rule_keys = ["event_rule_verb", "event_rule_name", "event_rule_no_of_attempts",
                       "event_rule_time_interval"]

    def __init__(cls):
        pass

    @classmethod
    def add_event(cls, event_noun):

        if EventBl.__check_if_event_exist(event_noun):
            print("EventBl | Event %s already exist's in db" % event_noun)
        else:
            EventDal.add_event(event_noun)

    @classmethod
    def add_rule_to_event(cls, event_rule, event_noun):

        if EventBl.__check_if_event_exist(event_noun):
            for key in cls.event_rule_keys:
                if key in event_rule:
                    print("EventBl | add_rule_to_event | The value of {} is {}".format(key, event_rule[key]))
                else:
                    raise ValueError("Please provide value for %s" % key)
        else:
            print("EventBl | add_rule_to_event | Event %s not found in db | Please provide valid event" % event_noun)

        if EventDal.is_event_rule_in_db(event_rule["event_rule_name"], event_rule["event_rule_verb"]):
            print("EventBl | add_rule_to_event | Rule {} with verb {} already exist in db".format(event_rule["event_rule_name"],
                                                                              event_rule["event_rule_verb"]))
        else:
            EventDal.add_rule_to_event(event_rule, event_noun)

    @staticmethod
    def execute_event_rule(event_rule_name=None, event_rule_verb=None):
        print("EventBl | Executing event rule")
        EventDal.add_execution_attempt(event_rule_name, event_rule_verb)
        EventBl.__check_and_store_json(event_rule_name, event_rule_verb)

    @staticmethod
    def get_event_data(page_number, no_of_items_per_page, event_noun=None, event_rule_name=None, event_rule_verb=None):
        if event_noun is not None:
            return EventDal.get_event_data(page_number, no_of_items_per_page, event_noun=event_noun)
        elif event_rule_verb is not None:
            return EventDal.get_event_data(page_number, no_of_items_per_page, event_rule_name=event_rule_name, event_rule_verb=event_rule_verb)
        else:
            return EventDal.get_event_data(page_number, no_of_items_per_page)


    @staticmethod
    def __check_and_store_json(event_rule_name, event_rule_verb):
        """
        It check's no of successive calls made to a particular event within a time interval.
        Store json if event rules are met.
        :param event_rule_name: Name of the event rule [String, Required]
        :param event_rule_verb: Name of the event verb [String, Required]
        :return: void
        """

        no_of_successive_calls = EventBl.__get_no_of_eventcalls_within_time_interval(event_rule_name, event_rule_verb)
        event_rule_info = EventDal.get_event_rule_info(event_rule_name, event_rule_verb)

        if no_of_successive_calls >= event_rule_info["event_rule_no_of_attempts"]:
            print("EventBl | Event with rule '{}' and verb '{}' got executed {} times within {} minutes".format(
                event_rule_name, event_rule_verb, no_of_successive_calls, event_rule_info["event_rule_no_of_attempts"]))

            event_noun_info = EventDal.get_event_info_from_id(event_rule_info["event_noun_id"])
            EventBl.__store_json_data(event_rule_info, event_noun_info)

        EventDal.remove_stale_executed_event(event_rule_name, event_rule_verb)

    @staticmethod
    def __check_if_event_exist(event_noun):
        return EventDal.is_event_in_db(event_noun)

    @staticmethod
    def __get_no_of_eventcalls_within_time_interval(event_rule_name, event_rule_verb):
        return EventDal.get_no_of_eventcalls_within_time_interval(event_rule_name, event_rule_verb)

    @staticmethod
    def __store_json_data(event_rule_info, event_noun_info):
        """
        Create and store a event json object
        :param event_rule_info: A dictionary object with required values [Dictionary, Required]
        :param event_noun_info: A list containing event noun information [List, Required]
        :return: void
        """
        event_custom_list = ["event_rule_verb", "event_rule_name"]
        jsonrep = {}
        for key in event_custom_list:
            if key == "event_rule_verb":
                jsonrep["verb"] = event_rule_info[key]
            if key == "event_rule_name":
                jsonrep["eventId"] = event_rule_info[key]

        jsonrep["noun"] = event_noun_info["event_noun"]
        jsonrep["timestamp"] = int(datetime.datetime.now().timestamp())

        # Dummy object data
        jsonrep["data"] = [{"id": 1, "value": "val1"}, {"id": 2, "value": "val2"}]
        EventDal.add_event_data(event_noun_info["event_id"], event_rule_info["event_rule_id"], json.dumps(jsonrep))
