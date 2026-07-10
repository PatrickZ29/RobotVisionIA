import os, sys, io
import M5
from M5 import *
from hardware import Pin
from m5espnow import M5ESPNow
import time

# Variables globales
boton1 = None
boton2 = None
estado_anterior_1 = 1
estado_anterior_2 = 1
espnow_0 = None
ID_DESTINO = 2 # Identificador interno para el dispositivo receptor

def setup():
  global boton1, boton2, estado_anterior_1, estado_anterior_2, espnow_0

  M5.begin()
  Widgets.fillScreen(0x000000)

  # 1. Configuramos los dos botones usando la librería 'hardware' de M5
  # Botón 1 en el pin 1, Botón 2 en el pin 2
  boton1 = Pin(1, mode=Pin.IN, pull=Pin.PULL_UP)
  boton2 = Pin(2, mode=Pin.IN, pull=Pin.PULL_UP)

  estado_anterior_1 = boton1.value()
  estado_anterior_2 = boton2.value()

  # 2. Configuramos ESP-NOW usando 'm5espnow'
  espnow_0 = M5ESPNow(0)

  # Registramos el receptor.
  espnow_0.set_add_peer('34B7DA573ACC', ID_DESTINO, 0, False)

  print("Sistema listo. Presiona los botones en los pines 1 o 2...")

def loop():
  global estado_anterior_1, estado_anterior_2, espnow_0

  M5.update()

  # Leemos el estado actual de ambos pines
  estado_actual_1 = boton1.value()
  estado_actual_2 = boton2.value()

  # --- LÓGICA PARA EL BOTÓN 1 ---
  if estado_actual_1 != estado_anterior_1:
      if estado_actual_1 == 0:
          print("¡Botón 1 presionado! Enviando 1 por M5ESPNow...")
          espnow_0.send_data(ID_DESTINO, 1)
      else:
          print("Botón 1 soltado.")
      # Actualizamos el estado
      estado_anterior_1 = estado_actual_1

  # --- LÓGICA PARA EL BOTÓN 2 ---
  if estado_actual_2 != estado_anterior_2:
      if estado_actual_2 == 0:
          print("¡Botón 2 presionado! Enviando 2 por M5ESPNow...")
          espnow_0.send_data(ID_DESTINO, 2)
      else:
          print("Botón 2 soltado.")
      # Actualizamos el estado
      estado_anterior_2 = estado_actual_2

  # Pequeña pausa para debounce (evitar falsos toques mecánicos)
  time.sleep_ms(50)

if __name__ == '__main__':
  try:
    setup()
    while True:
      loop()
  except (Exception, KeyboardInterrupt) as e:
    try:
      from utility import print_error_msg
      print_error_msg(e)
    except ImportError:
      print("please update to latest firmware")
