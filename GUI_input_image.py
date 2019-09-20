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


kivy.require("1.10.1")



class ConnectPage(GridLayout):
    # runs on initialization
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 2  # used for our grid

        if os.path.isfile("prev_detail.txt"):
            with open("prev_details.txt","r") as f:
                d = f.read().split(",")

                prev_username = d[0]
                prev_password = d[1]
                prev_image = d[2]
        else:
            prev_username = ""
            prev_password = ""
            prev_image = ""


        # Input Text box username
        self.add_widget(Label(text='Username:'))
        self.username = TextInput(text=prev_username, multiline=False)
        self.add_widget(self.username)

        # Input Text box Label
        self.add_widget(Label(text='Password:'))
        self.password = TextInput(text=prev_password, multiline=False)
        self.add_widget(self.password)

        # Input Text box image
        self.add_widget(Label(text='Image:'))
        self.image = TextInput(text=prev_image, multiline=False)
        self.add_widget(self.image)



        # add our button.
        self.join = Button(text="Join")
        self.join.bind(on_press=self.join_button)
        self.add_widget(Label())  # just take up the spot.
        self.add_widget(self.join)

    def join_button(self, instance):
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

        chat_app.img_page
        chat_app.screen_manager.current = 'Input Image'



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

        # load image
        #self.img = Image(source="/Users/suksomboon/Desktop/photo/Woman.jpg") # Image file name
        self.img = Image(source=words[-1])
        self.img.allow_stretch = True
        self.img.keep_ratio = False

        # Position set
        self.img.pos = (200,100)

        self.img.opacity = 1
        self.add_widget(self.img)





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

        # # Info page
        # self.info_page = InfoPage()
        # screen = Screen(name='Info')
        # screen.add_widget(self.info_page)
        # self.screen_manager.add_widget(screen)

        # Image page
        self.img_page = LoadImg()
        screen = Screen(name='Input Image')
        screen.add_widget(self.img_page)
        self.screen_manager.add_widget(screen)

        return self.screen_manager

if __name__ == "__main__":
    chat_app = ImageApp()
    chat_app.run()
