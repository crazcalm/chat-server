import help_text

import asyncio
import argparse
import logging


clients = []

class SimpleChatClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        self.peername = transport.get_extra_info("peername")
        self.name = "No Name"
        self.description = "None"
        logging.info("connection_made: {}".format(self.peername).encode())
        clients.append(self)

    def data_received(self, data):
        msg = data.decode().strip()
        logging.debug("data_received: {}".format(msg))

        if msg == "/disconnect":
            self.transport.close()
            logging.info("command: /quit")

        elif msg == "/whoami":
            logging.info("command: /whoami")
            self.transport.write("You are {}\n".format(self.name).encode())
            self.transport.write("Description: {}\n".format(
                self.description).encode())

        elif msg == "/people":
            logging.info("command: /people")
            people = [client for client in clients if client != self]
            for index, client in enumerate(people):
                self.transport.write("{}: {}\n".format(
                    index, client.name).encode()) 

        elif msg == "/chatroom":
            logging.info("command: /chatroom")

        elif msg == "/help":
            logging.info("command: /help")
            self.transport.write("{}".format(help_text.HELP_GENERAL).encode()) 

        elif msg.startswith("/whois "):
            command, name = msg.split(' ', 1)
            logging.info("command: {}\Args: {}".format(
                command, name))
            found = False
            for client in clients:
                if client.name.strip() == name.strip():
                    found = client
                    break

            if found:
                self.transport.write('Name: {}\nDescription: {}\n'.format(
                    found.name, found.description).encode())
            else:
                self.transport.write(
                    "I don't know\n".encode())

        elif msg.startswith("/msg "):
            args = msg.split(' ', 1)[1]
            name, direct_msg = args.split(',', 1)
            logging.info("command: /msg-{}, {}".format(name, direct_msg))

            found = False
            logging.debug("Looking for: {}".format(name))
            for client in clients:
                logging.debug("client: {}".format(client.name))
                # strip should happen somewhere else!
                if client.name.strip() == name.strip():
                    logging.debug("Found: {}".format(name))
                    found = client
                    break
            if found:
                client.transport.write('*{}\n'.format(
                    ' '.join(direct_msg.strip())).encode())
                self.transport.write('msg sent'.encode())
            else:
                logging.debug("Not Found: {}".format(name))
                self.transport.write('Could not find {}\n'.format(
                    name).encode())

        elif msg.startswith("/help "):
            command_args = msg.split(' ')[:2]
            logging.info("command: {}".format(command_args))
            error_msg = "{} is not a valid command".format(command_args[1])
            msg = help_text.HELP_DICT.get(command_args[1])
            self.transport.write(msg.encode())

        elif msg.startswith("/set "):
            command_args = msg.strip().split(' ')
            logging.info("command: {}\n".format(command_args))
            key, value = None, None
            if len(command_args) < 3:
                # not enough args for command.
                pass
            else:
                key, *value = command_args[1:]
            if key and value and key in ['name', 'description']:
                if key == 'name':
                    self.name = ' '.join(value)
                    self.transport.write(
                        "Name: {}\n".format(self.name).encode())
                elif key == 'description':
                    self.description = ' '.join(value)
                    self.transport.write("Description: {}\n".format(
                        self.description).encode())
            else:
                # something is wrong with the args
                pass            
        else:
            for client in clients:
                client.transport.write("{}: {}".format(self.peername, 
                    data.decode()).encode())

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
    
