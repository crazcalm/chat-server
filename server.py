import asyncio
import argparse


clients = []

class SimpleChatClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        self.peername = transport.get_extra_info("peername")
        print("connection_made: {}".format(self.peername))
        clients.append(self)

    def data_received(self, data):
        msg = data.decode()
        print("data_received: {}".format(msg))

                
        if msg.strip() == "/quit":
            self.transport.close()

        for client in clients:
            client.transport.write("{}: {}".format(self.peername, 
                data.decode()).encode())

    def connection_lost(self, ex):
        print("connection_lost: {}".format(self.peername))
        clients.remove(self)

def cli_parser():
    # logic for argparse
    chat_server = argparse.ArgumentParser(
        description="testing description",
        epilog="Tesing epilog")

    chat_server.add_argument(
        "--ip",
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

def run_server():
    # runs the server
    print("starting up..")

    loop = asyncio.get_event_loop()
    coro = loop.create_server(SimpleChatClientProtocol, port=3333, 
                host="127.0.0.1")
    server = loop.run_until_complete(coro)

    for socket in server.sockets:
        print("serving on {}".format(socket.getsockname()))

    loop.run_forever()

def main():
    # Logic for program
    pass


if __name__ == '__main__':
    cli_args = cli_parser()
    print(cli_args.parse_args())
