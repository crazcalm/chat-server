from unittest import TestCase

def before_scenario(context, scenario):
    context.test = TestCase()

def after_scenario(context, scenario):
    if hasattr(context, "chat_server"):
        if not context.chat_server.poll():
            context.chat_server.kill()
