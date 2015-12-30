from subprocess import Popen, PIPE
import shlex

"""
Note:
- After creating an instance of unittest.TestCase,
  I can use all of their assert statements!
"""

@given(u'I want to use port {port}')
def step_impl(context, port):
    context.command = shlex.split(
        "python3 server.py --port {}".format("port"))

@when(u'I start the chat server')
def step_impl(context):
    context.chat_server = Popen(context.command, stdout=PIPE)

@then(u'running the server should have {result} in its output')
def step_impl(context, result):
    output = "".join([string for string in context.chat_server.stdout])
    context.test.assertIn(result, output)

