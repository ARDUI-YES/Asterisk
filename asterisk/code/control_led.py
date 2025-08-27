#!/usr/bin/env python3
import syS
import serial
import time

# Initialiser le port série
ser = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(2)  # Attendre 2 secondes pour permettre à l'Arduino de se stabiliser

# Envoyer la commande à l'Arduino
ser.write(b'1')  # '1' pour allumer la LED
ser.close()
sys.exit(0)