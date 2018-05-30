from libevent.controller import EventController

USER_LOGIN_FAILURE_RULE = {"event_rule_name": "login-failed",
                           "event_rule_no_of_attempts": 5, "event_rule_time_interval": 10}
CONTENT_ACCESS_SUCCESS_RULE = {"event_rule_name": "access-success",
                               "event_rule_no_of_attempts": 5, "event_rule_time_interval": 2}


def add_event_info():

    event_obj.create_event("user-login","failed")
    event_obj.create_event("content-access", "success")


def add_event_rule():

    event_obj.add_rule_to_event(USER_LOGIN_FAILURE_RULE, event_noun="user-login", event_verb="failed")
    event_obj.add_rule_to_event(CONTENT_ACCESS_SUCCESS_RULE, event_noun="content-access", event_verb="success")


if __name__ == "__main__":

    event_obj = EventController()

    # Creates event
    print("===ADD EVENT===")
    add_event_info()
    print("\n")

    # Adds rules to event
    print("===ADD RULE TO EVENT===")
    add_event_rule()
    print("\n")

    # Gets all event data, with paging (page_number=1, no_of_items_per_page=100)
    print("===GET TOP 100 EVENT DATA | items_per_page=100 ===")
    print(event_obj.get_event_data(no_of_items_per_page=100))
    print("\n")

    # Gets filtered event data, with default paging (page_number=1, no_of_items_per_page=5)
    print("===GET FILTERED EVENT DATA | noun='content-access', verb='success, pg_num=1, items_per_page=3' ===")
    print(event_obj.get_event_data(event_noun="user-login", event_verb="failed", page_number=1, no_of_items_per_page=3))
    print("===GET FILTERED EVENT DATA | noun='content-access', verb='success, pg_num=2, items_per_page=3' ===")
    print(event_obj.get_event_data(event_noun="user-login", event_verb="failed", page_number=1, no_of_items_per_page=3))
    print("\n")