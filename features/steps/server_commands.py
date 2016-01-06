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
    context.person1.sendall(command.encode())
    # Give the server time to send response
    time.sleep(2)

@then(u'the client should receive {response}')
def step_impl(context, response):
    print("tesint: {}".format(response))
    output = context.person1.recv(2048).decode()
    context.test.assertIn(response, output)    

@then(u'the client socket should be disconnected')
def step_impl(context):
    context.person1.sendall("/disconnect".encode())
    # need to add an assert to make sure client is disconnected

@given(u'person2 is in the chatroom')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given person2 is in the chatroom')
    context.person2 = socket.create_connection(('localhost', 3333))
    context.person2.sendall('/set name Player 2'.encode())
