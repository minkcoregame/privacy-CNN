import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
# to use buttons:
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image, AsyncImage
import os
import socket_client # To use client_socket
import client_p3app_socket # To use client_cam.py and server_cam.py for server-client communication
from kivy.clock import Clock
import os
import sys

from kivy.uix.screenmanager import *
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.config import Config



kivy.require("1.10.1")

IP = "127.0.0.1"  # "127.0.0.1" is the standard loopback interface address (local host) (for server24 "172.16.24.1")
PORT = 1234        # Port to listen on (non-privileged ports are > 1023 and < 65535)


class ConnectPage(GridLayout):
    # runs on initialization
    # First page for getting user's information
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 2  # used for our grid

        if os.path.isfile("prev_detail.txt"):
            with open("prev_details.txt","r") as f:
                d = f.read().split(",")

                prev_ip = d[0]
                prev_port = d[1]
                prev_username = d[2]
                prev_password = d[3]
                prev_image = d[4]
        else:
            prev_ip = ""
            prev_port = ""
            prev_username = ""
            prev_password = ""
            prev_image = ""

        # Input Text box IP of a server
        self.add_widget(Label(text='IP:'))  # widget #1, top left
        self.ip = TextInput(text=prev_ip, multiline=False)  # defining self.ip...
        self.add_widget(self.ip)  # widget #2, top right

        # Input Text box Port of IP
        self.add_widget(Label(text='Port:'))
        self.port = TextInput(text=prev_port, multiline=False)
        self.add_widget(self.port)

        # Input Text box Username
        self.add_widget(Label(text='Username:'))
        self.username = TextInput(text=prev_username, multiline=False)
        self.add_widget(self.username)

        # Input Text box Password
        self.add_widget(Label(text='Password:'))
        self.password = TextInput(text=prev_password, multiline=False)
        self.add_widget(self.password)

        # Input Text box Image file location
        self.add_widget(Label(text='Input Image:'))
        self.image = TextInput(text=prev_image, multiline=False)
        self.add_widget(self.image)



        # add join button.
        # Click botton to submit info
        self.join = Button(text="Submit")
        self.join.bind(on_press=self.join_button) # action of join button
        self.add_widget(Label())
        self.add_widget(self.join)

    def join_button(self, instance):
        # Join button do
        ip = self.ip.text
        port = self.port.text
        username = self.username.text
        password = self.password.text
        image = self.image.text

        with open("prev_details.txt", "w") as f:
            f.write(f"{username},{password},{image}")
        # print(f"Joining {ip}:{port} as {username}")
        # Create info string, update InfoPage with a message and show it
        #info = f"Joining {ip}:{port} as {username} with {image}"
        #chat_app.info_page.update_info(info)
        #chat_app.screen_manager.current = 'Info'

        info = f"Joining {ip}:{port} as {username}"
        chat_app.info_page.update_info(info)
        chat_app.screen_manager.current = 'Info'
        Clock.schedule_once(self.connect, 1)

       # chat_app.img_page
       # chat_app.screen_manager.current = 'Input Image'
       # Clock.schedule_once(self.connect, 1)

    # Connects to the server
    # (second parameter is the time after which this function had been called,
    #  we don't care about it, but kivy sends it, so we have to receive it)
    def connect(self, _):

        # Get information for sockets client
        port = int(self.port.text)
        ip = self.ip.text
        username = self.username.text
        password = self.password.text

        if not client_p3app_socket.connect(ip, port, username, password,show_error):
            return

        #if not socket_client.connect(ip, port, username, show_error):
        #    return

        # Create chat page and activate it
        #chat_app.create_chat_page()
        chat_app.create_image_page()
        chat_app.screen_manager.current = 'Input Image'

# This class is an improved version of Label
# Kivy does not provide scrollable label, so we need to create one
class ScrollableLabel(ScrollView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # ScrollView does not allow us to add more than one widget, so we need to trick it
        # by creating a layout and placing two widgets inside it
        # Layout is going to have one collumn and and size_hint_y set to None,
        # so height wo't default to any size (we are going to set it on our own)
        self.layout = GridLayout(cols=1, size_hint_y=None)
        self.add_widget(self.layout)

        # Now we need two wodgets - Label for chat history and 'artificial' widget below
        # so we can scroll to it every new message and keep new messages visible
        # We want to enable markup, so we can set colors for example
        self.chat_history = Label(size_hint_y=None, markup=True)
        self.scroll_to_point = Label()

        # We add them to our layout
        self.layout.add_widget(self.chat_history)
        self.layout.add_widget(self.scroll_to_point)

    # Methos called externally to add new message to the chat history
    def update_chat_history(self, message):

        # First add new line and message itself
        self.chat_history.text += '\n' + message

        # Set layout height to whatever height of chat history text is + 15 pixels
        # (adds a bit of space at teh bottom)
        # Set chat history label to whatever height of chat history text is
        # Set width of chat history text to 98 of the label width (adds small margins)
        self.layout.height = self.chat_history.texture_size[1] + 15
        self.chat_history.height = self.chat_history.texture_size[1]
        self.chat_history.text_size = (self.chat_history.width * 0.98, None)

        # As we are updating above, text height, so also label and layout height are going to be bigger
        # than the area we have for this widget. ScrollView is going to add a scroll, but won't
        # scroll to the botton, nor there is a method that can do that.
        # That's why we want additional, empty wodget below whole text - just to be able to scroll to it,
        # so scroll to the bottom of the layout
        self.scroll_to(self.scroll_to_point)

    def update_chat_history_layout(self, _=None):
        # Set layout height to whatever height of chat history text is + 15 pixels
        # (adds a bit of space at the bottom)
        # Set chat history label to whatever height of chat history text is
        # Set width of chat history text to 98 of the label width (adds small margins)
        self.layout.height = self.chat_history.texture_size[1] + 15
        self.chat_history.height = self.chat_history.texture_size[1]
        self.chat_history.text_size = (self.chat_history.width * 0.98, None)



class ChatPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 2
        #self.add_widget(Label(text='Fancy stuff here to come!!!', font_size=30))

        # First row is going to be occupied by our scrollable label
        # We want it be take 90% of app height
        self.history = ScrollableLabel(height=Window.size[1]*0.9, size_hint_y=None)
        self.add_widget(self.history)

        # In the second row, we want to have input fields and Send button
        # Input field should take 80% of window width
        # We also want to bind button click to send_message method
        self.new_message = TextInput(width=Window.size[0] * 0.8, size_hint_x=None, multiline=False)
        self.send = Button(text="Send")
        self.send.bind(on_press=self.send_message)

        # To be able to add 2 widgets into a layout with just one collumn, we use additional layout,
        # add widgets there, then add this layout to main layout as second row
        bottom_line = GridLayout(cols=2)
        bottom_line.add_widget(self.new_message)
        bottom_line.add_widget(self.send)
        self.add_widget(bottom_line)

        # To be able to send message on Enter key, we want to listen to keypresses
        Window.bind(on_key_down=self.on_key_down)

        # We also want to focus on our text input field
        # Kivy by default takes focus out out of it once we are sending message
        # The problem here is that 'self.new_message.focus = True' does not work when called directly,
        # so we have to schedule it to be called in one second
        # The other problem is that schedule_once() have no ability to pass any parameters, so we have
        # to create and call a function that takes no parameters
        Clock.schedule_once(self.focus_text_input, 1)

        # And now, as we have out layout ready and everything set, we can start listening for incimmong messages
        # Listening method is going to call a callback method to update chat history with new messages,
        # so we have to start listening for new messages after we create this layout
        socket_client.start_listening(self.incoming_message, show_error)

        self.bind(size=self.adjust_fields)

    # Updates page layout

    def adjust_fields(self, *_):

        # Chat history height - 90%, but at least 50px for bottom new message/send button part
        if Window.size[1] * 0.1 < 50:
            new_height = Window.size[1] - 50
        else:
            new_height = Window.size[1] * 0.9
        self.history.height = new_height

        # New message input width - 80%, but at least 160px for send button
        if Window.size[0] * 0.2 < 160:
            new_width = Window.size[0] - 160
        else:
            new_width = Window.size[0] * 0.8
        self.new_message.width = new_width

        # Update chat history layout
        # self.history.update_chat_history_layout()
        Clock.schedule_once(self.history.update_chat_history_layout, 0.01)

    # Gets called on key press
    def on_key_down(self, instance, keyboard, keycode, text, modifiers):

        # But we want to take an action only when Enter key is being pressed, and send a message
        if keycode == 40:
            self.send_message(None)

    # Gets called when either Send button or Enter key is being pressed
    # (kivy passes button object here as well, but we don;t care about it)
    def send_message(self, _):
        #print("send a message!!!")
        # Get message text and clear message input field
        message = self.new_message.text
        self.new_message.text = ''

        # If there is any message - add it to chat history and send to the server
        if message:
            # Our messages - use red color for the name
            self.history.update_chat_history(f'[color=dd2020]{chat_app.connect_page.username.text}[/color] > {message}')
            socket_client.send(message) ## Sent the message out

        # As mentioned above, we have to shedule for refocusing to input field
        Clock.schedule_once(self.focus_text_input, 0.1)

   # Sets focus to text input field
    def focus_text_input(self, _):
        self.new_message.focus = True

    # Passed to sockets client, get's called on new message
    def incoming_message(self, username, message):
        # Update chat history with username and message, green color for username
        self.history.update_chat_history(f'[color=20dd20]{username}[/color] > {message}')


# Simple information/error page
class InfoPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Just one column
        self.cols = 1

        # And one label with bigger font and centered text
        self.message = Label(halign="center", valign="middle", font_size=30)

        # By default every widget returns it's side as [100, 100], it gets finally resized,
        # but we have to listen for size change to get a new one
        # more: https://github.com/kivy/kivy/issues/1044
        self.message.bind(width=self.update_text_width)

        # Add text widget to the layout
        self.add_widget(self.message)

    # Called with a message, to update message text in widget
    def update_info(self, message):
        self.message.text = message

    # Called on label width update, so we can set text width properly - to 90% of label width
    def update_text_width(self, *_):
        self.message.text_size = (self.message.width * 0.9, None)

class LoadImg(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Just one column
        self.cols = 1

        # Read file name from file
        with open("prev_details.txt","r") as f:
            data = f.readlines()

            for line in data:
                words =line.split(",")
            print(words)
            print(words[-1])
            Img_path = words[-1]

        # load image
        self.img = Image(source=words[-1])
        self.img.allow_stretch = True
        self.img.keep_ratio = False


        # Position set
        self.img.pos = (100,100)
        self.img.source = words[-1]

        self.img.opacity = 1
        self.add_widget(self.img)




        # add join button.
        self.encrypt = Button(text="Encrypt it!")
        self.encrypt.bind(on_press=self.encrypt_button)
        self.add_widget(self.encrypt)


    def encrypt_button(self, instance):

        #print("Encrypt it!")
        # Create info string, update InfoPage with a message and show it
        #info = f"Joining {ip}:{port} as {username} with {image}"
        #chat_app.info_page.update_info(info)
        #chat_app.screen_manager.current = 'Info'

        ## Do the enncryption here and send the image to the server

        client_p3app_socket.send_img(self.img.source)



        #chat_app.status_page
        #chat_app.screen_manager.current = 'Status'
        Clock.schedule_once(self.connect, 1)

    def connect(self, _):

        # Create chat page and activate it
        chat_app.create_status_page()
        chat_app.screen_manager.current = 'Status'

class StatusPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Just one column
        self.cols = 1


        # And one label with bigger font and centered text
        self.message = Label(halign="center", valign="middle", font_size=30)

        # By default every widget returns it's side as [100, 100], it gets finally resized,
        # but we have to listen for size change to get a new one
        # more: https://github.com/kivy/kivy/issues/1044
        self.message.bind(width=self.update_text_width)

        # Add text widget to the layout
        self.add_widget(Button(text="I am encrypting your image and sending to a server!"))

        # Called with a message, to update message text in widget



    def update_info(self, message):
        self.message.text = message

        # Called on label width update, so we can set text width properly - to 90% of label width

    def update_text_width(self, *_):
        self.message.text_size = (self.message.width * 0.9, None)

    def send_img_2_server(self, _):

        # call the client_im_socket.py
        clientclient_p3app_socket.send_img()





class ImageApp(App):
    def build(self):
        # We are going to use screen manager, so we can add multiple screens
        # and switch between them
        self.screen_manager = ScreenManager()

        # Initial, connection screen (we use passed in name to activate screen)
        # First create a page, then a new screen, add page to screen and screen to screen manager
        self.connect_page = ConnectPage()
        screen = Screen(name='Connect')
        screen.add_widget(self.connect_page)
        self.screen_manager.add_widget(screen)

        # Info page
        self.info_page = InfoPage()
        screen = Screen(name='Info')
        screen.add_widget(self.info_page)
        self.screen_manager.add_widget(screen)


        # Image page
        self.img_page = LoadImg()
        screen = Screen(name='Input Image')
        screen.add_widget(self.img_page)
        self.screen_manager.add_widget(screen)

        # Status page
        self.status_page = StatusPage()
        screen = Screen(name="Status")
        screen.add_widget(self.status_page)
        self.screen_manager.add_widget(screen)




        return self.screen_manager

    # We cannot create chat screen with other but screens, as its init method will start listening
    # for incoming connections, but at this stage connection is not being made yet, so we
    # call this method later
    def create_chat_page(self):
        self.chat_page = ChatPage()
        screen = Screen(name='Chat')
        screen.add_widget(self.chat_page)
        self.screen_manager.add_widget(screen)

    def create_image_page(self):
        self.img_page = LoadImg()
        screen = Screen(name='Input Image')
        screen.add_widget(self.img_page)
        self.screen_manager.add_widget(screen)

    def create_status_page(self):
        self.status_page = StatusPage()
        screen = Screen(name="Status")
        screen.add_widget(self.status_page)
        self.screen_manager.add_widget(screen)


# Error callback function, used by sockets client
# Updates info page with an error message, shows message and schedules exit in 10 seconds
# time.sleep() won't work here - will block Kivy and page with error message won't show up
def show_error(message):
    chat_app.info_page.update_info(message)
    chat_app.screen_manager.current = 'Info'
    Clock.schedule_once(sys.exit, 10)



if __name__ == "__main__":
    chat_app = ImageApp()
    chat_app.run()