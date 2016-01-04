HELP_DISCONNECT = """
/diconnect: Disconnects you from the chat server.
"""

HELP_WHOAMI = """
/whoami: Returns your chat room name.
"""

HELP_PEOPLE = """
/people: Returns the ame of the people in the chat server.
"""

HELP_CHATROOM = """
/chatroom: Returns the names of the chat room.
"""

HELP_HELP = """
- /help displays the list of commands and properties that you can interact 
with.

- /help [command]: shows the doc for that specific command.
"""

HELP_WHOIS = """
/whois [name]: returns the description of the persion
"""

HELP_MSG = """
/msg [name]: sends a direct message to that person
"""

HELP_SET = """
/set [property] [value]: Set the value of a specific property
"""

HELP_GENERAL = """

All commands start with a "/".

Command List:
- /disconnect: Disconnects you from the chat server
- /whoami: Returns your chat room name
- /people: Returns the names of the people in the chat room
- /chatroom: Returns the name of the chat room
- /help: I am not sure what to write here...
- /help [command]: Shows the docs for the specified command 
- /whois [name]: returns the description of that person
- /msg [name]: sends a direct message to that person
- /set [property] [value]: Set the value of a specified property

Property List:
- name
- description
"""

HELP_DICT = {
    'disconnect': HELP_DISCONNECT,
    'whoami': HELP_WHOAMI,
    'people': HELP_PEOPLE,
    'chatroom': HELP_CHATROOM,
    'help': HELP_HELP,
    'whois': HELP_WHOIS,
    'msg': HELP_MSG,
    'set': HELP_SET
}
