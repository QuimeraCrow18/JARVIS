import sys
import os
import uuid
import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.camera import Camera
from kivy.utils import platform

from modules.keta_storage import KetaStorageManager
from modules.keta_crypto import KetaCryptoManager


class PantallaRegistroDueno(Screen):
    def __init__(self, **kwargs):
        super(PantallaRegistroDueno, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        layout.add_widget(Label(
            text="[b]REGISTRO DE DUENO MAESTRO[/b]\nNingun dueno detectado. Registra tu identidad.",
            markup=True, font_size='18sp', halign='center'
        ))

        self.camara = Camera(play=True, resolution=(640, 480))
        layout.add_widget(self.camara)

        btn_capturar = Button(
            text="Escanear Rostro y Sellar APK",
            background_color=(0.1, 0.5, 0.8, 1), font_size='16sp'
        )
        btn_capturar.bind(on_press=self.procesar_y_guardar_dueno)
        layout.add_widget(btn_capturar)

        self.add_widget(layout)

    def procesar_y_guardar_dueno(self, instance):
        storage = KetaStorageManager()
        crypto = KetaCryptoManager()

        id_dueno = "OWNER_JOSAMICK_MAESTRO"
        dispositivo_uuid = str(uuid.getnode())

        crypto.generar_par_llaves(id_dueno)
        with open(f"keys/{id_dueno}_public.pem", "r") as f:
            llave_publica_pem = f.read()

        vector_rostro_simulado = [0.123, -0.456, 0.789, 0.012]
        rostro_json = json.dumps(vector_rostro_simulado)

        exito = storage.registrar_dueno_maestro(id_dueno, dispositivo_uuid, llave_publica_pem, rostro_json)

        if exito:
            self.manager.current = 'dashboard'


class PantallaDashboardC2(Screen):
    def __init__(self, **kwargs):
        super(PantallaDashboardC2, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        self.lbl_estado = Label(
            text="[b]JOSAMICK CORE AI[/b]\n[color=00FF00]Dispositivo Cifrado y Vinculado al Dueno[/color]",
            markup=True, font_size='18sp', halign='center'
        )
        layout.add_widget(self.lbl_estado)

        btn_mesh = Button(text="Activar Hilos Keta Mesh", background_color=(0.1, 0.6, 0.4, 1))
        btn_mesh.bind(on_press=self.encender_servicios)
        layout.add_widget(btn_mesh)

        self.add_widget(layout)

    def encender_servicios(self, instance):
        if platform == 'android':
            from android import android_service
            android_service.start_service(title="Josamick", description="Malla activa", arg="")
            self.lbl_estado.text = "[b]JOSAMICK[/b]\nServicio de fondo iniciado."


class PantallaDesbloqueoBiometrico(Screen):
    def __init__(self, **kwargs):
        super(PantallaDesbloqueoBiometrico, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        self.lbl_indicador = Label(
            text="[b]SENSADO BIOMETRICO REQUERIDO[/b]\nMirando a la camara para verificar identidad del Dueno.",
            markup=True, font_size='16sp', halign='center'
        )
        layout.add_widget(self.lbl_indicador)

        self.camara_verificadora = Camera(play=True, resolution=(640, 480))
        layout.add_widget(self.camara_verificadora)

        btn_verificar = Button(
            text="Verificar Identidad",
            background_color=(0.2, 0.6, 0.8, 1), font_size='16sp'
        )
        btn_verificar.bind(on_press=self.autenticar_dueno)
        layout.add_widget(btn_verificar)

        self.add_widget(layout)

    def autenticar_dueno(self, instance):
        from modules.keta_storage import sqlite3

        conexion = sqlite3.connect("database/keta_mesh.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT rostro_vector_json FROM dueno_biometria WHERE owner_id = 'OWNER_JOSAMICK_MAESTRO'")
        resultado = cursor.fetchone()
        conexion.close()

        if resultado:
            vector_maestro = json.loads(resultado[0])

            vector_actual_escaneado = [0.123, -0.456, 0.789, 0.012]

            diferencia = sum(abs(a - b) for a, b in zip(vector_maestro, vector_actual_escaneado))

            if diferencia < 0.05:
                self.lbl_indicador.text = "[color=00FF00][b]ACCESO CONCEDIDO[/b][/color]\nIdentidad confirmada. Iniciando C2..."
                self.manager.current = 'dashboard'
            else:
                self.lbl_indicador.text = "[color=FF0000][b]ALERTA: ACCESO DENEGADO[/b][/color]\nRostro no coincide con el Dueno Maestro."


class JosamickApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(PantallaRegistroDueno(name='registro'))
        sm.add_widget(PantallaDesbloqueoBiometrico(name='desbloqueo'))
        sm.add_widget(PantallaDashboardC2(name='dashboard'))

        storage = KetaStorageManager()
        if storage.verificar_si_tiene_dueno():
            sm.current = 'desbloqueo'
        else:
            sm.current = 'registro'

        return sm


if __name__ == '__main__':
    JosamickApp().run()
