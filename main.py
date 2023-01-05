from random import randint
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
from kivymd.toast import toast
from kivy.utils import platform

import os
import cv2
import numpy
import requests
import json
import time
import mysql.connector


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

        MDFloatingActionButton:
            id: capture_button
            icon: 'camera'
            md_bg_color: "red"
            on_press: app.capture()
            pos_hint: {"center_x": 0.90, "center_y": 0.15}
            
            
    MDBottomNavigationItem:
        id: database
        name: "base de datos"
        text: "Análisis de datos"
        icon: "database"
        on_tab_press: app.rev_placa()
        FloatLayout:
            BoxLayout:
                orientation: 'vertical'
                padding: dp(20)
                MDLabel:
                    text: "Datos escaneados"
                    pos_hint: {'x':0, 'top':1}
                    halign: 'left'
                    valign: 'top'
                    font_style: "H4"
                    padding: "4dp", "4dp"
                MDTextField:
                    id: num_placa
                    hint_text: "Placa"
                    theme_text_color: "Secondary"
                MDTextField:
                    id: ubicacion
                    hint_text: "Ubicación"
                    theme_text_color: "Secondary"
                MDTextField:
                    id: active_type
                    hint_text: "Tipo de Activo"
                    theme_text_color: "Secondary"    
                MDTextField:
                    id: descrip
                    hint_text: "Descripción"
                    theme_text_color: "Secondary"

        MDFloatingActionButton:
            icon: "send"
            md_bg_color: app.theme_cls.primary_color
            pos_hint: {"center_x": 0.90, "center_y": 0.09}
            padding: "4dp", "4dp"
            on_press: app.registar_placa()


        

        

"""

class Inventario(MDApp):
    #Función que captura lo que está viendo la cámara
    def capture(self):
        camera = self.root.ids.camera
        id_number = randint(0, 1000000)
        name = 'photo' + str(id_number) + '.png'
        directorio_actual = os.getcwd()
        print(directorio_actual)
        camera.export_to_png(str(directorio_actual)+name)
        self.captura_actual = name
        '''
        Se va a correr la función de escaneo de OCR aquí para 
        que cuando el usuario ingrese directamente a la base de datos ya encuentre ahí
        la placa escaneada
        '''
        result = self.ocr_scan()
        if result == True:
            toast('Avance a la pestaña de inventario o capture de nuevo')
        elif result == False:
            toast("Objetivo no válido, por favor escanee de nuevo")

        


    #Función que realiza el escaneo de la cámara
    def ocr_scan(self):
        try:
            url = 'https://app.nanonets.com/api/v2/OCR/Model/34353217-1d3f-4511-b86f-e24e842e66e8/LabelFile/?async=false'
            data = {'file': open(self.captura_actual, 'rb')}

            response = requests.post(url, auth=requests.auth.HTTPBasicAuth('0DeaHQHCf7qAs9n7mFAGmF9gHd6IVMA9', ''), files=data)

            response_json = response.text
            response_json = json.loads(response_json)
            self.placa_actual = response_json["result"][0]['prediction'][0]['ocr_text']

            return True
        except:
            return False


    def rev_placa(self):
        db = mysql.connector.connect(
                host='localhost',
                user='root',
                passwd='InventarioEIE2409',
                database='inventarioeie'
            )
        mycursor = db.cursor()
        mycursor.execute("SELECT * FROM Activos")

        for elements in mycursor:
            if elements[0] == self.placa_actual:
                self.is_registered = True
            else:
                pass

        if self.is_registered == True:
            toast("La placa se encuentra registrada, edite los datos o capture de nuevo.")
            mycursor.execute("SELECT * FROM Activos WHERE placa = (%s)", (self.placa_actual,))
            #Editando los valores vacíos en el tab de la base de datos:
            self.root.ids.num_placa.text = self.placa_actual
            for i in mycursor:
                flag_list = i
            self.root.ids.ubicacion.text = flag_list[1]
            self.root.ids.active_type.text = flag_list[2]
            self.root.ids.descrip.text = flag_list[3]

        else:
            self.root.ids.num_placa.text = self.placa_actual
            toast("El activo no se encuentra registrado, registrelo por favor")


    def registar_placa(self):
        db = mysql.connector.connect(
                host='localhost',
                user='root',
                passwd='InventarioEIE2409',
                database='inventarioeie'
            )
        mycursor = db.cursor()
        
        if self.is_registered == True:
            mycursor.execute("UPDATE Activos SET ubicacion = %s, tipo_de_activo = %s, descripcion = %s WHERE placa = %s", (self.root.ids.ubicacion.text, self.root.ids.active_type.text, self.root.ids.descrip.text, self.placa_actual))
            db.commit()
            toast("Placa actualizada!")

        else:
            mycursor.execute("INSERT INTO Activos (placa, ubicacion, tipo_de_activo, descripcion) VALUES (%s, %s, %s, %s)", (self.placa_actual, self.root.ids.ubicacion.text, self.root.ids.active_type.text, self.root.ids.descrip.text))
            db.commit()
            toast("Placa registrada!")
    



    def build(self):
        self.theme_cls.material_style = 'M3'
        self.theme_cls.theme_style = "Light"
        self.captura_actual = ''
        self.placa_actual = ''
        self.is_registered = False


        screen = Builder.load_string(layouts)
        
        return screen

    
        
    
    


Inventario().run()
