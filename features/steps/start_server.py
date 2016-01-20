from subprocess import Popen, PIPE
import shlex
import time

"""
Note:
- After creating an instance of unittest.TestCase,
  I can use all of their assert statements!
"""
def read_server_log():
    with open("server_log", "r") as f:
        contexts = f.read()
    return contexts

@given(u'I want to use port {port}')
def step_impl(context, port):
    assert isinstance(int(port), int)
    #context.command = shlex.split(
    #    "python3 server.py --port {}".format("port"))
    context.command = ["python3", "server.py", "--port", str(int(port))]    

@when(u'I start the chat server')
def step_impl(context):
    context.chat_server = Popen(context.command, stdout=PIPE)
    # let the program start up
    time.sleep(3)

@then(u'running the server should have {result} in its output')
def step_impl(context, result):
    if 'success' in result:
        expected = 'serving on'

    output = read_server_log()
    context.test.assertIn(expected, output)

