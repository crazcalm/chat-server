import help_text

import asyncio
import argparse
import logging


clients = []

class SimpleChatClientProtocol(asyncio.Protocol):

    def __init__(self, name):
        self.chatroom_name = name

    def _send_msg(self, client, msg):
        client.transport.write("{}: {}\n".format(self.name,
            msg).encode())

    def _send_to_self(self, msg):
        self.transport.write("{}\n".format(msg).encode())

    def _unique_name(self, name):
        logging.debug("Is the name {} unique?".format(name))
        result = True
        for client in clients:
            logging.debug("Checking against: {}".format(client.name))
            if name == client.name:
                result = False
                break
        logging.debug("unique: {}".format(result))
        return result

    def connection_made(self, transport):
        self.transport = transport
        self.peername = transport.get_extra_info("peername")
        self.name = "No Name"
        self.description = "None"
        logging.info("connection_made: {}".format(self.peername).encode())
        clients.append(self)

    def send_to_everyone(self, msg):
        for client in clients:
            self._send_msg(client, msg)

    def find_client_by_name(self, name):
        found = None
        for client in clients:
            if client.name.strip() == name and client != self:
                found = client
                break
        return found


    def send_to_list_of_people(self, people):
        for client in people:
            self._send_msg(client, msg)

    def data_received(self, data):
        msg = data.decode().strip()
        logging.debug("data_received: {}".format(msg))

        if msg == "/disconnect":
            self.transport.close()
            logging.info("command: /quit")

        elif msg == "/whoami":
            logging.info("command: /whoami")
            self._send_to_self("You are {}\n".format(self.name))
            self._send_to_self("Description: {}\n".format(
                self.description))

        elif msg == "/people":
            logging.info("command: /people")
            people = [client for client in clients if client != self]
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
            msg = help_text.HELP_DICT.get(command_args[1])
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
                    else:
                        self._send_to_self(
                            "The name you selected is all ready in use." 
                            "\nPlease select another name.")
                elif key == 'description':
                    logging.debug('seeting description to {}'.format(value))
                    self.description = ' '.join(value)
                    self._send_to_self("Description: {}".format(
                        self.description))
            else:
                self._send_to_self(help_text.HELP_SET)
        else:
            self.send_to_everyone(msg)

    def connection_lost(self, ex):
        logging.info("connection_lost: {}".format(self.peername))
        clients.remove(self)

def cli_parser():
    # logic for argparse
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
    # runs the server
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
