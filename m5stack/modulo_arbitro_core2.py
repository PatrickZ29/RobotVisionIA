import os, sys, io
import M5
from M5 import *
from m5espnow import M5ESPNow
import time
import struct
import binascii

# --- VARIABLES GLOBALES ---
espnow_0 = None
ID_DESTINO = 1

# Estado de la interfaz
pantalla_actual = "competidores"
ultimo_toque = 0

# Variables de Alerta (Pantalla Competidores)
alerta_activa = 0
tiempo_parpadeo = 0
estado_color_rojo = False

# Estado del LED de respuesta (Pantalla Control)
# 0: apagado, 1: verde (recibido 8), 2: rojo (recibido 9)
estado_led = 0

# --- FUNCIONES DE DIBUJO (PANTALLA COMPETIDORES) ---
def dibujar_mitad_superior(estado):
    if estado == "listo":
        M5.Lcd.fillRect(10, 10, 300, 105, 0x1C4587)
        M5.Lcd.setTextColor(0xFFFFFF, 0x1C4587)
        M5.Lcd.setTextSize(7)
        M5.Lcd.drawString("1", 135, 30)
    elif estado == "limpiar":
        M5.Lcd.fillRect(10, 10, 300, 105, 0x000000)

def dibujar_mitad_inferior(estado):
    if estado == "listo":
        M5.Lcd.fillRect(10, 125, 300, 105, 0x1C4587)
        M5.Lcd.setTextColor(0xFFFFFF, 0x1C4587)
        M5.Lcd.setTextSize(7)
        M5.Lcd.drawString("2", 135, 145)
    elif estado == "limpiar":
        M5.Lcd.fillRect(10, 125, 300, 105, 0x000000)

# --- FUNCIÓN DE DIBUJO DEL LED (SOLO EN CONTROL) ---
def dibujar_led_control():
    global estado_led, pantalla_actual
    if pantalla_actual == "control":
        # Recuadro en la parte superior izquierda
        x, y, w, h = (10, 10, 50, 35)
        if estado_led == 1:   # Verde
            M5.Lcd.fillRect(x, y, w, h, 0x3CA242)
            M5.Lcd.drawRect(x, y, w, h, 0xFFFFFF)
        elif estado_led == 2: # Rojo
            M5.Lcd.fillRect(x, y, w, h, 0xE66A6A)
            M5.Lcd.drawRect(x, y, w, h, 0xFFFFFF)
        else:                # Apagado / Borde
            M5.Lcd.fillRect(x, y, w, h, 0x000000)
            M5.Lcd.drawRect(x, y, w, h, 0x555555)

# --- FUNCIÓN DE DIBUJO (PANTALLA DE CONTROL) ---
def dibujar_pantalla_control():
    M5.Lcd.fillScreen(0x000000)

    # Dibujar el LED de respuesta según su estado actual
    dibujar_led_control()

    # 1. Batería en la esquina superior derecha
    try:
        bateria = M5.Power.getBatteryLevel()
    except:
        bateria = 100

    M5.Lcd.setTextSize(2)
    M5.Lcd.setTextColor(0xFF9999, 0x000000)
    M5.Lcd.drawString(f"{bateria}%", 190, 15)

    # 2. Botón INICIAR (Verde)
    M5.Lcd.fillRect(20, 60, 130, 130, 0x1B431D)
    M5.Lcd.drawRect(20, 60, 130, 130, 0x3CA242)
    M5.Lcd.setTextColor(0xFFFFFF, 0x1B431D)
    M5.Lcd.setTextSize(3)
    M5.Lcd.drawString("Iniciar", 30, 110)

    # 3. Botón PAUSAR (Rojo)
    M5.Lcd.fillRect(170, 60, 130, 130, 0x4B2222)
    M5.Lcd.drawRect(170, 60, 130, 130, 0xE66A6A)
    M5.Lcd.setTextColor(0xFFFFFF, 0x4B2222)
    M5.Lcd.setTextSize(3)
    M5.Lcd.drawString("Pausar", 185, 110)

# --- FUNCIÓN CALLBACK DE RECEPCIÓN ESP-NOW ---
def cb_recepcion(espnow_obj):
    global alerta_activa, pantalla_actual, estado_led
    mac, data = espnow_obj.recv_data()

    try:
        valor = struct.unpack('<i', data)[0]

        # --- Lógica de los nuevos estados del LED ---
        if valor == 8:
            estado_led = 1 # Verde
            dibujar_led_control()
            return # Salimos para no interferir con la lógica de pantallas de abajo
        elif valor == 9:
            estado_led = 2 # Rojo
            dibujar_led_control()
            return

        # --- Lógica original de competidores ---
        if pantalla_actual == "control" and valor in [1, 2, 3, 4]:
            M5.Lcd.fillScreen(0x000000)
            pantalla_actual = "competidores"

        if valor == 1:
            if alerta_activa != 0:
                M5.Lcd.fillScreen(0x000000)
                alerta_activa = 0
            dibujar_mitad_superior("listo")
        elif valor == 2:
            if alerta_activa != 0:
                M5.Lcd.fillScreen(0x000000)
                alerta_activa = 0
            dibujar_mitad_inferior("listo")
        elif valor == 3:
            alerta_activa = 1
        elif valor == 4:
            alerta_activa = 2
        else:
            alerta_activa = 0
            if pantalla_actual == "competidores":
                M5.Lcd.fillScreen(0x000000)

    except Exception as e:
        print("Error al procesar:", e)

# --- CONFIGURACIÓN INICIAL ---
def setup():
    global espnow_0
    M5.begin()
    M5.Lcd.fillScreen(0x000000)

    espnow_0 = M5ESPNow(0)
    espnow_0.set_irq_callback(cb_recepcion)

    # REEMPLAZAR CON LA MAC DE TU DESTINO
    espnow_0.set_add_peer('34B7DA573ACC', ID_DESTINO, 0, False)

    print("Core2 Listo. LED de respuesta habilitado en Control.")

# --- BUCLE PRINCIPAL ---
def loop():
    global espnow_0, alerta_activa, tiempo_parpadeo, estado_color_rojo, pantalla_actual, ultimo_toque

    M5.update()

    # --- CAMBIO DE PANTALLAS (BOTONES FÍSICOS) ---
    if M5.BtnB.wasPressed():
        pantalla_actual = "control"
        dibujar_pantalla_control()

    if M5.BtnA.wasPressed():
        alerta_activa = 0
        pantalla_actual = "competidores"
        M5.Lcd.fillScreen(0x000000)

    # --- LÓGICA TÁCTIL (SOLO EN CONTROL) ---
    if M5.Touch.getCount() > 0 and (time.ticks_ms() - ultimo_toque > 400):
        try:
            x = M5.Touch.getX()
            y = M5.Touch.getY()

            if pantalla_actual == "control":
                # Botón INICIAR
                if 20 <= x <= 150 and 60 <= y <= 190:
                    espnow_0.send_data(ID_DESTINO, 1)
                    M5.Lcd.drawRect(20, 60, 130, 130, 0xFFFFFF)
                    time.sleep_ms(100)
                    M5.Lcd.drawRect(20, 60, 130, 130, 0x3CA242)

                # Botón PAUSAR
                elif 170 <= x <= 300 and 60 <= y <= 190:
                    espnow_0.send_data(ID_DESTINO, 2)
                    M5.Lcd.drawRect(170, 60, 130, 130, 0xFFFFFF)
                    time.sleep_ms(100)
                    M5.Lcd.drawRect(170, 60, 130, 130, 0xE66A6A)

        except Exception as e:
            print("Error táctil:", e)
        ultimo_toque = time.ticks_ms()

    # --- LÓGICA DE PARPADEO (SOLO EN COMPETIDORES) ---
    if alerta_activa > 0 and pantalla_actual == "competidores":
        if time.ticks_ms() - tiempo_parpadeo > 300:
            tiempo_parpadeo = time.ticks_ms()
            estado_color_rojo = not estado_color_rojo

            color_fondo = 0xFF0000 if estado_color_rojo else 0x000000
            M5.Lcd.fillScreen(color_fondo)
            M5.Lcd.setTextColor(0xFFFFFF, color_fondo)
            M5.Lcd.setTextSize(10)
            M5.Lcd.drawString(str(alerta_activa), 120, 80)

    time.sleep_ms(20)

if __name__ == '__main__':
    try:
        setup()
        while True:
            loop()
    except Exception as e:
        print("Error en ejecución:", e)
