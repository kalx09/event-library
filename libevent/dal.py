from libevent.db_connection import db_obj
import json


class EventDal:
    """A database layer: Interacts with mysql database"""

    def __init__(self):
        pass

    ####################################################################################################

    ADD_EVENT = "INSERT INTO event_info (event_noun, event_verb, created_by_rule) VALUES (%s, %s, %s);"
    GET_LAST_ID = "SELECT LAST_INSERT_ID() as id"

    @staticmethod
    def add_event(event_noun, event_verb, custom_event):
        """
        Add's event to db
        :param event_noun: Name of the unique event [String, Required]
        :param event_verb: Name of the event verb [String, Required]
        :return: void
        """
        db_obj.execute(EventDal.ADD_EVENT, (event_noun, event_verb, custom_event))
        result_set = db_obj.execute(EventDal.GET_LAST_ID, ())
        return result_set.get_rows()[0]["id"]

    ####################################################################################################

    GET_EVENT_ID = "SELECT event_id FROM event_info WHERE LOWER(event_noun) = LOWER(%s);"
    GET_EVENT_ID_FROM_NOUN_VERB = "SELECT event_id FROM event_info WHERE LOWER(event_noun) = LOWER(%s) " \
                                  "and LOWER(event_verb) = LOWER(%s)"
    GET_EVENT_NOUN = "SELECT * from event_info where event_id = %s"

    @staticmethod
    def get_event_id_from_noun_verb(event_noun, event_verb):
        """
        Check's whether provided event name exit's in db
        :param event_noun: Name of the event [String, Required]
        :param event_verb: Name of the event verb [String, Required]
        :return: event_id: Event Id if found else -1 [Integer]
        """
        result_set = db_obj.execute(EventDal.GET_EVENT_ID_FROM_NOUN_VERB, (event_noun, event_verb))
        if result_set.has_row():
            return result_set.get_rows()[0]["event_id"]
        else:
            return -1

    @staticmethod
    def get_event_info_from_id(event_id):
        """
        Retrieves event information
        :param event_id: Associated event id
        :return: A list object with event information [List]
        """
        result_set = db_obj.execute(EventDal.GET_EVENT_NOUN, (event_id,))
        return result_set.get_rows()[0]

    @staticmethod
    def get_event_id_from_noun(event_noun):
        """
        Retrieves event id from the event noun
        :param event_noun: Name of the event
        :return: Event id [Integer]
        """
        result_set = db_obj.execute(EventDal.GET_EVENT_ID, (event_noun,))
        return result_set.get_rows()[0]["event_id"]

    ####################################################################################################

    ADD_RULE_TO_EVENT = "INSERT into event_rule (event_rule_name, event_rule_no_of_attempts, " \
                        "event_rule_time_interval, event_noun_id) VALUES (%s, %s, %s, %s);"

    @staticmethod
    def add_rule_to_event(event_rule, event_noun, event_verb):
        """
        Add's rule to the event
        :param event_rule: Name of the event rule. It needs to be unique [String. Required]
        :param event_noun: Name of the event [String, Required]
        :param event_verb: Name of the existing event verb. Eg., "failed" [String, Required]
        :return: A dictionary object
                 event_noun_id: Holds the event id [Integer]
                 event_rule_id: Holds the event rule id [Integer]
        """
        event_result_set = db_obj.execute(EventDal.GET_EVENT_ID_FROM_NOUN_VERB, (event_noun, event_verb))
        if event_result_set.has_row():
            event_noun_id = event_result_set.get_rows()[0]["event_id"]
            db_obj.execute(EventDal.ADD_RULE_TO_EVENT, (event_rule["event_rule_name"],
                                                        int(event_rule["event_rule_no_of_attempts"]),
                                                        int(event_rule["event_rule_time_interval"]),
                                                        event_noun_id))
            result_set = db_obj.execute(EventDal.GET_LAST_ID, ())
            return event_noun_id, result_set.get_rows()[0]["id"]

    ####################################################################################################

    GET_EVENT_RULE_INFO_FROM_ID = "SELECT * FROM event_rule WHERE event_rule_id = %s;"
    GET_EVENT_RULE_ID_FROM_NOUN_ID = "SELECT event_rule_id FROM event_rule WHERE event_noun_id = %s;"
    GET_EVENT_RULE_ID = "SELECT * FROM event_rule WHERE LOWER(event_rule_name) = LOWER(%s);"

    @staticmethod
    def is_event_rule_in_db(event_rule_name):
        """
        Check's whether provided event rule exit's in db
        :param event_rule_name: Name of the event rule [String, Required]
        :return: True: If event rule exist
                 False: If event rule oes not exist
        """
        result_set = db_obj.execute(EventDal.GET_EVENT_RULE_ID, (event_rule_name))
        return True if result_set.has_row() else False

    @staticmethod
    def get_event_rule_info(event_rule_id):
        """
        Retrieve's event rule information
        :param event_rule_id: Event rule id [Integer, Required]
        :return: A list object with event rule information
        """
        result_set = db_obj.execute(EventDal.GET_EVENT_RULE_INFO_FROM_ID, event_rule_id)
        return result_set.get_rows()[0]

    @staticmethod
    def get_event_rule_id_from_noun_id(event_id):
        """
        Retrieve's event rule id
        :param event_id: Noun event id [Integer, Required]
        :return: Event rule id [Integer]
        """
        result_set = db_obj.execute(EventDal.GET_EVENT_RULE_ID_FROM_NOUN_ID, event_id)
        if result_set.has_row():
            return result_set.get_rows()[0]["event_rule_id"]
        else:
            return -1

    ####################################################################################################

    GET_ALL_EVENTS_WITHIN_TIME_INTERVAL = "SELECT * FROM event_data WHERE event_noun_id = %s and " \
                                          "TIMESTAMP > NOW() - INTERVAL %s MINUTE"

    @staticmethod
    def get_no_of_eventcalls_within_time_interval(event_noun_id, event_rule_id):
        """
        Retrieve no of calls made for a specific event rule
        :param event_noun_id: Event id [Integer, Required]
        :param event_rule_id: Event rule id [Integer, Required]
        :return: Count of calls [Integer]
        """
        event_rule_result_set = db_obj.execute(EventDal.GET_EVENT_RULE_INFO_FROM_ID, event_rule_id)
        if event_rule_result_set.has_row():
            event_row_set = event_rule_result_set.get_rows()
            event_rule_time_interval = event_row_set[0]["event_rule_time_interval"]
            result_set = db_obj.execute(EventDal.GET_ALL_EVENTS_WITHIN_TIME_INTERVAL,
                                        (event_noun_id, event_rule_time_interval))
            return result_set.row_count()

    ####################################################################################################

    ADD_EVENT_DATA = "INSERT INTO event_data (event_noun_id, event_data_json_rep) VALUES (%s, %s)"
    GET_EVENT_DATA = "SELECT event_data_json_rep FROM event_data %s LIMIT %s OFFSET %s"

    @staticmethod
    def add_event_data(event_noun_id, json_rep):
        """
        Add's event data to db
        :param event_noun_id: Event id of the event for which data is required to be stored [Integer, Required]
        :param json_rep: Event data [String, Required]
        :return: void
        """
        db_obj.execute(EventDal.ADD_EVENT_DATA, (event_noun_id, json_rep))

    @staticmethod
    def get_event_data(page_number, no_of_items_per_page, event_noun=None, event_verb=None):
        """
        Retrieve's event data of the provided event noun, rule or verb
        :param page_number: Page number to be fetched [Integer, Optional]
        :param no_of_items_per_page: Number of items to retrieve on each page [Integer, Optional]
        :param event_noun: Name of the event [String, Optional]
        :param event_verb: Name of the event verb [String, Optional]
        :return: A list object of event data [List]
        """
        offset = no_of_items_per_page * (page_number - 1)
        limit = no_of_items_per_page
        event_data_list = []
        where_clause = ""
        if event_noun is not None:
            where_clause = "WHERE event_noun_id = %s" % EventDal.get_event_id_from_noun(event_noun)
        elif event_verb is not None:
            where_clause = "WHERE event_noun_id = %s" % EventDal.get_event_id_from_noun_verb(event_noun, event_verb)

        result_set = db_obj.execute(EventDal.GET_EVENT_DATA % (where_clause, limit, offset))
        if result_set.has_row():
            data_set = result_set.get_rows()
            for data_obj in data_set:
                d=json.loads((data_obj["event_data_json_rep"]))
                event_data_list.append(d)

        return event_data_list
