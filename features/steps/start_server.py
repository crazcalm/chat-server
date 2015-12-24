@given(u'I want to use port 3333')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given I want to use port 3333')

@when(u'I start the chat server')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I start the chat server')

@then(u'running the server should "success"')
def step_impl(context):
    raise NotImplementedError(
        u'STEP: Then running the server should "success"')

@given(u'I want to use port 80')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given I want to use port 80')

@then(u'running the server should "failure"')
def step_impl(context):
    raise NotImplementedError(
        u'STEP: Then running the server should "failure"')
