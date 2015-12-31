from unittest import TestCase

def before_scenario(context, scenario):
    print("BEFORE {}".format(scenario))
    context.test = TestCase()

def after_scenario(context, scenario):
    print("AFTER {}".format(scenario))
    if hasattr(context, "chat_server"):
        if not context.chat_server.poll():
            context.chat_server.kill()
