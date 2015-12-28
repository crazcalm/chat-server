from subprocess import Popen, PIPE
import shlex

"""
Note:
- After creating an instance of unittest.TestCase,
  I can use all of their assert statements!
"""

@given(u'I want to use port <port>')
def step_impl(context, port):
    raise NotImplementedError(
        u'STEP: Given I want to use port {}'.format(port))
    command = shlex.split("python3 server.py --port {}".format("port"))
    context.chat_server = Popen(command, stdout=PIPE)

@when(u'I start the chat server')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I start the chat server')
    command = shlex.split("python3 server.py")
    context.chat_server = Popen(command, stdout=PIPE)

@then(u'running the server should have <result> in its output')
def step_impl(context, result):
    raise NotImplementedError(
        u'STEP: Then running the server should {}'.format(result))
    output = "".join([string for string in context.chat_server.stdout]

