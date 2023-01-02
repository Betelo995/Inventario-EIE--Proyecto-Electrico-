from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.uix.image import Image
from kivymd.uix.button import MDFillRoundFlatButton, MDFillRoundFlatIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
from kivymd.theming import ThemeManager
from kivymd.uix.transition.transition import MDSlideTransition
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
import numpy
from random import randint
import requests
import json


layouts = """
MDBottomNavigation:
    panel_color: "#0ec3f3"
    selected_color_background: "#000000"
    text_color_active: "E1F5FE"

    MDBottomNavigationItem: 
        id: home
        name: "home"
        text: "Inicio"
        icon: "home"
        Image:
            source: "logo.png"
            pos_hint: {'center_x': 0.5, 'center_y': 0.9}
    MDBottomNavigationItem:
        id: capture_screen
        name: "capture"
        text: "Capturar"
        icon: "camera"
        Camera:
            id: camera
            resolution: (1080, 1080)
            play: True
        Button:
            text: 'Capturar'
            size_hint_y: None
            height: '48dp'
            on_press: app.capture()
            
            
    MDBottomNavigationItem: 
        id: xd
        name: "process"
        text: "Análisis de datos"
        icon: "database"
"""

class Inventario(MDApp):
    def capture(self):
        camera = self.root.ids.camera
        id_number = randint(0, 1000000)
        name = 'photo' + str(id_number) + '.png'
        camera.export_to_png("D:/Users/Isaac/Documents/Proyecto_Electrico/inventario/" + name)
        self.captura_actual = name
        print(name)

    def ocr_scan(self):
        url = 'https://app.nanonets.com/api/v2/OCR/Model/34353217-1d3f-4511-b86f-e24e842e66e8/LabelFile/?async=false'
        data = {'file': open(self.captura_actual, 'rb')}

        response = requests.post(url, auth=requests.auth.HTTPBasicAuth('0DeaHQHCf7qAs9n7mFAGmF9gHd6IVMA9', ''), files=data)

        response_json = response.text
        response_json = json.loads(response_json)
        self.placa_actual = response_json["result"][0]['prediction'][0]['ocr_text']



    def build(self):
        self.theme_cls.material_style = 'M3'
        self.theme_cls.theme_style = "Light"
        self.captura_actual = ''
        self.placa_actual = ''
        screen = Builder.load_string(layouts)
        
        
        
        return screen

    
        
    
    


Inventario().run()
