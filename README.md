#Chat Server

##Overview
	I wanted to learn more about asyncio, sockets, and
    GTK+, so I started building a chat server and client.
    Currently, I am focused on building the chat server.
    Once that has reached a state where I am satified with
    it, I will shift gears and work on the chat client.

##Dependencies
* python3.4 and up
* behave
* GTK+: On Ubuntu install via apt-get for python3

##Chat commands:
	All commands start with a "/".

	Command List:
	- /disconnect: Disconnects you from the chat server
	- /whoami: Returns your chat room name
	- /people: Returns the names of the people in the chat room
	- /chatroom: Returns the name of the chat room
	- /help: Displays help text about commands
	- /help [command]: Shows the docs for the specified command
	- /whois [name]: returns the description of that person
	- /msg [name]: sends a direct message to that person
	- /set [property] [value]: Set the value of a specified property

	Property List:
	- name
	- description

##Starting the Chat Server
	python server.py -h

	optional arguments:
  	-h, --help   show this help message and exit
  	--host HOST  IP Address
  	--port PORT  The port the app will use
  	--name NAME  Names the chat room
