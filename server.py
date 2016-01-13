import help_text

import asyncio
import argparse
import logging


clients = []

class SimpleChatClientProtocol(asyncio.Protocol):
    def _send_msg(self, client, msg):
        client.transport.write("{}: {}\n".format(self.name,
            msg).encode())

    def _send_to_self(self, msg):
        self.transport.write("{}\n".format(msg).encode())

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
            if client.name.strip() == name:
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
                    logging.debug('setting name to {}'.format(value))
                    self.name = ' '.join(value)
                    self._send_to_self("Name: {}".format(self.name))
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
        description="testing description",
        epilog="Tesing epilog")

    chat_server.add_argument(
        "--host",
        type=str,
        default="localhost",
        help="IP Address?")

    chat_server.add_argument(
        "--port",
        type=int,
        default=3333,
        help="The port the app will use?")

    chat_server.add_argument(
        "--name",
        type=str,
        default="Chat Room",
        help="Names the chat room")

    return chat_server

def run_server(host, port):
    # runs the server
    logging.info("starting up..")
    host = "127.0.0.1" if host == "localhost" else host

    loop = asyncio.get_event_loop()
    coro = loop.create_server(SimpleChatClientProtocol, port=port, 
                host=host)
    server = loop.run_until_complete(coro)

    for socket in server.sockets:
        logging.info("serving on {}".format(socket.getsockname()))

    loop.run_forever()

def main():
    logging.basicConfig(
        filename="server_log",
        filemode="w",
        level=logging.DEBUG
    )
    cli_args = cli_parser().parse_args()
    run_server(cli_args.host, cli_args.port)
    


if __name__ == '__main__':
    cli_args = cli_parser()
    test = cli_args.parse_args()
    main()

