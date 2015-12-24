@given(u'I came connected to the chat server as person1')
def step_impl(context):
    raise NotImplementedError(
        u'STEP: Given I came connected to the chat server as person1')

@when(u'the client sends {command}')
def step_impl(context, command):
    raise NotImplementedError(
        u'STEP: When the client sends {}'.format(command))

@then(u'the client should receive {response}')
def step_impl(context, response):
    raise NotImplementedError(
        u'STEP: Then the client should receive {}'.format(response))

@then(u'the client socket should be disconnected')
def step_impl(context):
    raise NotImplementedError(
        u'STEP: Then the client socket should be disconnected')

@given(u'person2 is in the chatroom')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given person2 is in the chatroom')
