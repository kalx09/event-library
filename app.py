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

    add_event_info("user-login")
    add_event_rule(USER_LOGIN_FAILURE_RULE, "user-login")

    do_login_fail(event_rule_name="login-failed", event_rule_verb="failed")

    print(event_obj.get_event_data())
    # event_obj.get_event_data(event_noun="content-access")
    # event_obj.get_event_data(event_rule_name="login-failed", event_rule_verb="failed")