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

	usage: server.py [-h] [--host HOST] [--port PORT] [--name NAME]

	This is a Basic Chat Server

	optional arguments:
  	-h, --help   show this help message and exit
  	--host HOST  selects the ip the chat server will be running on
  	--port PORT  selects the port that the chat server will run on
  	--name NAME  selects a name for the chatroom

	I hope you enjoy :D

##Using Netcat to connect to the Server
	Basic command: nc [ip] [port]

    By default, the chat server starts on localhost
    port 3333. To connect via netcat, use the below command.
    - nc localhost 333

##How to run the tests
	Running the behave command from the root directory
    will run the test. Depending on how you have
    installed behave, one of the two following command
    will work.

    - behave
    or
    - python -m behave

##How to run test with test coverage
	python -m coverage run -m behave

	Note:This will give you test coverage of the tests.

##Coverage reports
* html: coverage html
* terminal: coverage report

##Helpful References
* behave website: [add website]
* GTK+ python docs: [add website]
* Netcat tutorial: [add website]