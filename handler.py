from gi.repository import Gtk

import asyncio
import threading


class ThreadLoop(threading.Thread):
    def __init__(self, loop):
        threading.Thread.__init__(self)
        self.loop = loop

    def run(self):
        print("starting Thread")
        self.loop.run_forever()
        print("Ending Thread")


class ClientProtocol(asyncio.Protocol):
    def __init__(self, text_buf, loop):
        self.text_buf = text_buf
        self.loop = loop
        self.trasport = None

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        iter_end = self.text_buf.get_end_iter()
        self.text_buf.insert(iter_end, "\n{}".format(data.decode()))

    def connection_lost(self, exc):
        iter_end = self.text_buf.get_end_iter()
        self.text_buf.insert(iter_end, "\n disconnected")
        self.transport.close()
        print("transport has closed")
        print(dir(self.loop))
        print("self.loop.stop()")
        print(self.loop.stop())

    def send_msg(self, message):
        self.transport.write(message.encode())


class Handler:
    def __init__(self, text_entry, text_box):
        self.text_entry = text_entry
        self.text_box = text_box
        self.text_buf = self.text_box.get_buffer()

    def connect_button_clicked(self, widget):
        print("connect button clicked")
        self.loop = asyncio.get_event_loop()
        coro = self.loop.create_connection(lambda: ClientProtocol(
                self.text_buf, self.loop), '127.0.0.1', 3333)

        self.transport, self.protocol = self.loop.run_until_complete(coro)
        self.thread = ThreadLoop(self.loop)
        self.thread.start()

    def send_button_clicked(self, widget):
        print("sending")
        text = self.text_entry.get_text()
        # end_iter = self.text_buf.get_end_iter()
        if self.loop.is_running():
            print("loop is running")
            self.transport.write(text.encode())
        else:
            print("loop is not running")
            self.tranport = None


builder = Gtk.Builder()
builder.add_from_file("chat_test.glade")

window = builder.get_object("window1")
window.connect("delete-event", Gtk.main_quit)

text_entry = builder.get_object("text_entry")
text_box = builder.get_object("textbox")

builder.connect_signals(Handler(text_entry, text_box))

window.show_all()

Gtk.main()
