import cv2
from plyer import filechooser
import pytesseract as pytesseract
import speech_recognition as sr
from kivy.clock import Clock
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.config import Config

Config.set('graphics', 'resizable', True)
sm = ScreenManager()


class FirstScreen(Screen):
    def __init__(self, **kwargs):
        super(FirstScreen, self).__init__(**kwargs)
        Window.clearcolor = (255 / 255, 170 / 255, 5 / 255, 1)
        self.cont = FloatLayout()

        self.img = Image(
            source='./microphone.png',
            size_hint=(0.5, 0.5),
            pos_hint={'center_x': 0.5, 'center_y': 0.6}
        )
        self.label = Label(
            text="WRITE FOR ME",
            font_size='35sp',
            font_family='3.ttf',
            color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.5, 'center_y': .9}
        )
        self.btnSpeech = Button(
            text="START",
            size_hint=(.5, .1),
            background_color='blue',
            font_size='20sp',
            font_family='3.ttf',
            color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.5, 'center_y': .3}
        )
        self.btnSpeech.bind(on_press=self.goToLoading)
        self.me = Label(
            text="(C) Mohamed Abdirahman Abdullahi",
            font_size='16sp',
            font_family='3.ttf',
            color=(.3, .3, .3, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.1}
        )

        self.cont.add_widget(self.img)
        self.cont.add_widget(self.label)
        self.cont.add_widget(self.me)
        self.cont.add_widget(self.btnSpeech)

        self.add_widget(self.cont)

    def goToLoading(self, instance):
        sm.add_widget(LoadingScreen(name="LoadingScreen"))
        sm.current = "LoadingScreen"


class LoadingScreen(Screen):
    def __init__(self, **kwargs):
        super(LoadingScreen, self).__init__(**kwargs)
        Window.clearcolor = (255 / 255, 170 / 255, 5 / 255, 1)
        self.loadImg = Image(
            source='./output-onlinegiftools.gif',
            size_hint=(0.4, 0.4),
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            anim_delay=.1,
            allow_stretch=True
        )
        self.progress = ProgressBar(
            max=10,
            value=0,
            size_hint=(0.8, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.4}
        )
        Clock.schedule_interval(self.count, .2)
        self.add_widget(self.loadImg)
        self.add_widget(self.progress)

    def count(self, instance):
        self.progress.value += 1
        if self.progress.value == 10:
            Clock.stop_clock()
            self.progress.value = 0
            sm.add_widget(MainScreen(name="MainScreen"))
            sm.current = "MainScreen"


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        Window.clearcolor = (0, 0, 0, 1)
        self.btnCont = FloatLayout()
        self.btnRecord = Button(
            background_normal='microphone.jpg',
            size_hint=(.23, .16),
            pos_hint={'center_x': .725, 'center_y': 0.05}
        )
        self.btnRecord.bind(on_press=self.record)
        self.btnUpload = Button(
            background_normal='upload.png',
            size_hint=(.14, .1),
            pos_hint={'center_x': 0.27, 'center_y': 0.05}
        )
        self.btnUpload.bind(on_press=self.upload_image)

        self.btnCont.add_widget(self.btnUpload)
        self.btnCont.add_widget(self.btnRecord)
        self.title = Label(
            text="Ready To Write For You",
            size_hint=(1, .2),
            font_size="28sp",
            color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.5, 'center_y': .965}
        )
        self.textInput = TextInput( hint_text="Output",
                                    readonly=False,
                                    size_hint=(1, .8),
                                    halign='center',
                                    font_size="40sp",
                                    background_color=(255 / 255, 170 / 255, 5 / 255, 1),
                                    foreground_color=(1, 1, 1, 1),
                                    pos_hint={'center_x': 0.5, 'center_y': .52}
                                    )
        self.add_widget(self.btnCont)
        self.add_widget(self.textInput)
        self.add_widget(self.title)

    def record(self, instance):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print('Listening')
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        try:
            print('Recognizing')
            command = r.recognize_google(audio, language='en-uk')
            self.textInput.font_size = '20sp'
            if self.textInput.text == "":
                self.textInput.text = command
            else:
                self.textInput.text += " " + command
        except Exception as e:
            print(e)
            self.textInput.text = "sorry! something went wrong!!! \nplease try again..."

    def remove_noise(self, image):
        return cv2.medianBlur(image, 1)

    def convert(self, source):
        print(source)
        try:
            img = cv2.imread(source)
            update = self.remove_noise(img)
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(update, config=custom_config)
            self.textInput.font_size = '18sp'
            self.textInput.text += text
        except:
            pass

    def upload_image(self, instance):
        filename = filechooser.open_file(title="Choose pdfs to merge",
                                         multiple=True,
                                         )
        if filename is not None:
            self.convert(filename[0])


class WriteForMe(App):
    def build(self):
        self.icon = 'microphone.png'

        sm.add_widget(FirstScreen(name="FirstScreen"))

        return sm


if __name__ == "__main__":
    WriteForMe().run()
