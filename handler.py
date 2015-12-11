from gi.repository import Gtk

class Handler:
    def __init__(self, text_entry, text_box):
        self.text_entry = text_entry
        self.text_box = text_box
        self.text_buf = self.text_box.get_buffer()

    def connect_button_clicked(self, widget):
        print("connect button clicked")
        print(self)

    def disconnect_button_clicked(self, widget):
        print("disconnect button clicked")
        print("Quiting app")
        Gtk.main_quit()

    def send_button_clicked(self, widget):
        print("sending")
        text = self.text_entry.get_text()
        end_iter = self.text_buf.get_end_iter()
        self.text_buf.insert(end_iter, text)


builder = Gtk.Builder()
builder.add_from_file("chat_test.glade")

window = builder.get_object("window1")
window.connect("delete-event", Gtk.main_quit)

text_entry = builder.get_object("text_entry")
text_box = builder.get_object("textbox")

builder.connect_signals(Handler(text_entry, text_box))


# testing
#print("dir(Builder) : {}".format(dir(builder)))

print("dir(text_entry): {}".format(dir(text_entry)))
text_entry.insert_text("Testing this out", 0)

window.show_all()

Gtk.main()
