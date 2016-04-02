import help_text

import asyncio
import argparse
import logging
from random import randint
from time import sleep

clients = []


class SimpleChatClientProtocol(asyncio.Protocol):
    """
    This class is the heart of the Chat Server. For each client that
    connects to the server, an instance of this class is created. These
    instances are saved in a global list.
    """

    def __init__(self, name):
        self.chatroom_name = name
        self.client = False

    def _send_msg(self, person, msg, format=True):
        """
        This method sends messages clients to other clients
        in the chatroom.

        Args:
            person (SimpleChatClientProtocol): A chat server client
            msg (str): message to be sent
        """
        if format:
            person.transport.write("{}: {}\n".format(self.name,
                                   msg).encode())
        else:
            person.transport.write("{}\n".format(msg).encode())

    def _send_to_self(self, msg, client=False):
        """
        This method sends messages to self. Typically used for
        help dialogs and other interactions that are meant only
        for this client.

        Args:
            msg (str): message to be sent
        """
        if client:
            self.transport.write("CLIENT**: {}".format(msg).encode())
        else:
            self.transport.write("{}\n".format(msg).encode())

    def _send_to_clients(self, msg):
        for person in clients:
            if person.client:
                person._send_to_self(msg, client=True)

    def _unique_name(self, name):
        """
        This method checks to see if the name that was passed
        in as a parameter is unique among the names of the
        clients in the chatroom.

        Args:
            name (str): a potential name

        Return:
            str or false: Returns False or name, which is Truthy
        """
        logging.debug("Is the name {} unique?".format(name))
        result = True
        for client in clients:
            logging.debug("Checking against: {}".format(client.name))
            if name == client.name and self != client:
                result = False
                break
        logging.debug("unique: {}".format(result))
        return result

    def connection_made(self, transport):
        """
        This method designates what will happen when a client
        makes a connection to the server.

        Args:
            transport (socket): The incoming socket from the client
        """
        self.transport = transport
        self.peername = transport.get_extra_info("peername")
        self.name = "No Name"
        while not self._unique_name(self.name):
            self.name += str(randint(0, 9))
        self.description = "None"
        logging.info("connection_made: {}".format(self.peername).encode())
        clients.append(self)
        self._send_to_self("Welcome to {}!".format(self.chatroom_name))
        self._send_to_self("To see the options available to you type `/help`")
        self._send_to_self("Your username name is: {}".format(self.name))
        self.send_to_everyone("<--- {} joined the room".format(self.name),
                              format=False)
        self._send_to_clients(self.client_user_list())

    def send_to_everyone(self, msg, format=True):
        """
        This method sends a message to everyone in the chatroom.

        Args:
            msg (str): The message to be sent
        """
        for client in clients:
            self._send_msg(client, msg, format=format)

    def find_client_by_name(self, name):
        """
        This method attempts to find a client that has a
        name that matches the name passed into the method.
        If the client is found, a reference to that client
        is returned. If the client is not found, then a None
        object is returned.

        Args:
            name (str): The name used in the search

        Returns:
            False or client: False or client, which is truthy
        """
        found = None
        for client in clients:
            if client.name.strip() == name:
                found = client
                break
        return found

    def send_to_list_of_people(self, people, msg):
        """
        This method sends a message to a list of people.

        Args:
            people (list): list of clients
            msg (str): The message to be sent
        """
        # Currently not used. If I dediced to add groups
        # to the app, then I will use this method.
        for person in people:
            self._send_msg(person, msg)

    def data_received(self, data):
        """
        This method is in charge of receiving the data that
        has been sent from the client. The rules for how
        this data is dealt with exist here.

        Args:
            data (byte): The data received over the socket connection
        """
        msg = data.decode().strip()
        logging.debug("data_received: {}".format(msg))

        if msg == "/disconnect":
            self.send_to_everyone("---> {} left the room".format(self.name),
                                  format=False)
            self.transport.close()
            logging.info("command: /quit")

            # Update client lists
            self._send_to_clients(self.client_user_list())

        elif msg == "/whoami":
            logging.info("command: /whoami")
            self._send_to_self("You are {}\n".format(self.name))
            self._send_to_self("Description: {}\n".format(
                self.description))

        elif msg == "/people":
            logging.info("command: /people")
            people = [client for client in clients if client != self]
            if not people:
                self._send_to_self("****No one else is in the room....*****")
            for index, client in enumerate(people):
                self._send_to_self("{}: {}\n".format(index, client.name))

        elif msg == "/chatroom":
            logging.info("command: /chatroom")
            self._send_to_self("Chatroom name: {}".format(
                                self.chatroom_name))

        elif msg == "/help":
            logging.info("command: /help")
            self._send_to_self("{}".format(help_text.HELP_GENERAL))

        elif msg.startswith("/whois "):
            if len(msg.split(' ')) >= 2:
                command, name = msg.split(' ', 1)
                logging.info("command: {}\Args: {}".format(
                    command, name))

                found = self.find_client_by_name(name.strip())

                if found:
                    self._send_to_self('Name: {}\nDescription: {}'.format(
                        found.name, found.description))
                else:
                    self._send_to_self("I don't know")
            else:
                self._send_to_self(help_text.HELP_WHOIS)

        elif msg.startswith("/msg "):
            if len(msg.split(' ')) and ',' in msg:
                args = msg.split(' ', 1)[1]
                name, direct_msg = args.split(',', 1)
                logging.info("command: /msg-{}, {}".format(name, direct_msg))

                found = self.find_client_by_name(name.strip())

                if found:
                    direct_msg = ''.join(direct_msg.strip())
                    self._send_msg(found, "*{}".format(direct_msg))
                    self._send_to_self('msg sent')
                else:
                    logging.debug("Not Found: {}".format(name))
                    self._send_to_self('Could not find {}'.format(name))
            else:
                self._send_to_self(help_text.HELP_MSG)

        elif msg.startswith("/help "):
            command_args = msg.split(' ')[:2]
            logging.info("command: {}".format(command_args))
            error_msg = "{} is not a valid command".format(command_args[1])
            msg = help_text.HELP_DICT.get(command_args[1], error_msg)
            self._send_to_self(msg)

        elif msg.startswith("/set "):
            command_args = msg.strip().split(' ')
            logging.info("command: {}\n".format(command_args))
            key, value = None, None
            if len(command_args) >= 3 and\
                    command_args[1] in ['name', 'description']:
                key, *value = command_args[1:]
                if key == 'name':
                    name = ' '.join(value)
                    if self._unique_name(name):
                        logging.debug('setting name to {}'.format(value))
                        self.name = name
                        self._send_to_self("Name: {}".format(self.name))
                        self._send_to_clients(self.client_user_list())
                    else:
                        self._send_to_self(
                            "The name you selected is all ready in use."
                            "\nPlease select another name.")
                elif key == 'description':
                    logging.debug('setting description to {}'.format(value))
                    self.description = ' '.join(value)
                    self._send_to_self("Description: {}".format(
                        self.description))
            else:
                self._send_to_self(help_text.HELP_SET)

        elif msg.startswith("/CLIENT**: USER LIST"):
            if self.client:
                logging.debug("/CLIENT**: USER LIST")
                self._send_to_self(self.client_user_list(), client=True)
            else:
                logging.debug("A non-client called: /CLIENT**: USER LIST")

        elif msg.startswith("/CLIENT**: TRUE"):
            logging.debug("/CLIENT**: TRUE")
            self.client = True
            self._send_to_self(self.client_user_list(), client=True)

        else:
            self.send_to_everyone(msg)

    def client_user_list(self):
        sleep(1)
        logging.debug("method: client_user_list")
        user_list = [client.name for client in clients]
        return ",".join(user_list)

    def connection_lost(self, ex):
        """
        This method fires when the connections between
        the client and server is lost.

        Args:
            ex (I do not know): I should learn what you are...
        """
        logging.info("connection_lost: {}".format(self.peername))
        clients.remove(self)

        # Update clients
        self._send_to_clients(self.client_user_list())


def cli_parser():
    """
    This function contains the logic for the command line
    parser.
    """
    chat_server = argparse.ArgumentParser(
        description=help_text.CLI.get('description'),
        epilog=help_text.CLI.get('epilog'))

    chat_server.add_argument(
        "--host",
        type=str,
        default="localhost",
        help=help_text.CLI.get('host'))

    chat_server.add_argument(
        "--port",
        type=int,
        default=3333,
        help=help_text.CLI.get('port'))

    chat_server.add_argument(
        "--name",
        type=str,
        default="Chat Room",
        help=help_text.CLI.get('name'))

    return chat_server


def run_server(host, port, name):
    """
    This function is charge of running the server.

    Args:
        host (str): host name/ip address
        port (int): port to which the app will run on
        name (str): the name of the chatroom
    """
    logging.info("starting up..")
    print("Server running on {}:{}".format(host, port))
    host = "127.0.0.1" if host == "localhost" else host

    loop = asyncio.get_event_loop()
    coro = loop.create_server(lambda: SimpleChatClientProtocol(name),
                              port=port, host=host)
    server = loop.run_until_complete(coro)

    for socket in server.sockets:
        logging.info("serving on {}".format(socket.getsockname()))

    loop.run_forever()


def main():
    """
    This function contains the logic for the logger
    and is in charge of running this application.
    """
    logging.basicConfig(
        filename="server_log",
        filemode="w",
        level=logging.DEBUG,
        format='%(asctime)s--%(levelname)a--%(funcName)s--%(name)s:%(message)s'
    )
    cli_args = cli_parser().parse_args()
    run_server(cli_args.host, cli_args.port, cli_args.name)


if __name__ == '__main__':
    cli_args = cli_parser()
    test = cli_args.parse_args()
    main()
