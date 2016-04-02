import socket
import time
from subprocess import Popen, PIPE


@given(u'I came connected to the chat server as person1')
def step_impl(context):
    context.chat_server = Popen(["python", "server.py"], stdout=PIPE)
    # Give the server time to start
    time.sleep(3)
    context.person1 = socket.create_connection(('localhost', 3333))

@when(u'the client sends {command}')
def step_impl(context, command):
    context.person1.sendall(command.strip().encode())
    # Give the server time to send response
    time.sleep(3)

@then(u'the client should receive {response}')
def step_impl(context, response):
    time.sleep(3)
    output = context.person1.recv(2048).decode()
    context.test.assertIn(response, output)

@then(u'the client socket should be disconnected')
def step_impl(context):
    context.person1.sendall("/disconnect".encode())

@given(u'person2 is in the chatroom')
def step_impl(context):
    context.person2 = socket.create_connection(('localhost', 3333))
    context.person2.sendall('/set name M'.encode())
    time.sleep(5)
    context.person2.sendall('/set description friend'.encode())
    context.person2.sendall('/whoami'.encode())
    output = context.person2.recv(1024)
    context.test.assertIn('M', output.decode())

@when(u'person2 leaves the chatroom')
def step_impl(context):
    context.person2.sendall('/disconnect'.encode())

@given(u'I am connected to the server via a client application')
def step_impl(context):
    context.person1.sendall('/CLIENT**: TRUE'.encode())
