from libevent.controller import EventController

USER_LOGIN_FAILURE_RULE = {"event_rule_verb": "failed", "event_rule_name": "login-failed",
                           "event_rule_no_of_attempts": 5, "event_rule_time_interval": 1}


def add_event_info(event_noun):

    event_obj.create_event(event_noun)


def add_event_rule(event_rule_info, event_noun):

    event_obj.add_rule_to_event(event_rule_info, event_noun)


def do_login_fail(event_rule_name, event_rule_verb):
    event_obj.execute_event_rule(event_rule_name, event_rule_verb)


if __name__ == "__main__":
    event_obj = EventController()

    # Creates 'user-login' event
    print("===ADD EVENT===")
    add_event_info("user-login")
    print("\n")

    # Adds rule to 'user-login' event
    print("===ADD RULE TO EVENT===")
    add_event_rule(USER_LOGIN_FAILURE_RULE, "user-login")
    print("\n")

    # Executes 'user-login' event with 'failed' verb
    print("===EXECUTE EVENT===")
    do_login_fail(event_rule_name="login-failed", event_rule_verb="failed")
    print("\n")

    # Gets all event data, with default paging (page_number=1, no_of_items_per_page=5)
    print("===GET EVENT DATA===")
    print(event_obj.get_event_data())
    print("\n")

    # Gets filtered event data, with default paging (page_number=1, no_of_items_per_page=5)
    print("===GET FILTERED EVENT DATA===")
    print(event_obj.get_event_data(event_rule_name="login-failed", event_rule_verb="failed"))
    print("\n")