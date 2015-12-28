from unittest import TestCase

def before_all(context):
    print("BEFORE ALL")
    context.test = TestCase()

def after_all(context):
    print("AFTER ALL")
    if hasattr(context, "chat_server"):
        if not context.chat_server.poll():
            context.chat_server.kill()
