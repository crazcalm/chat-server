@given(u'I want to use port <port>')
def step_impl(context, port):
    raise NotImplementedError(
        u'STEP: Given I want to use port {}'.format(port))

@when(u'I start the chat server')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I start the chat server')

@then(u'running the server should have <result> in its output')
def step_impl(context, result):
    raise NotImplementedError(
        u'STEP: Then running the server should {}'.format(result))

