# Import necessary libraries for camera and BME280
import camera
import os
import time
import machine
from machine import I2C, Pin
from struct import unpack
from time import sleep
from BME280_Class import BME280

print("start")
scl = Pin( 13 )
sda = Pin( 12 )

i2c = I2C( 0,scl=scl,sda=sda,freq=100000)
i2cDevices = i2c.scan()

print( "List of I2C devices found during scan:" )

for device in i2cDevices:
    print( "Found device 0x%02x   (dec: %d)" % (device,device) )
    pass

bme = BME280(i2c)

import network 

ssid = 'Livebox-6FB4_EXT'
password = '4Cz3Fdznv4nZJZDSTD'

def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to Wi-Fi network...")
        wlan.connect(ssid, password)

        # Wait for the connection
        while not wlan.isconnected():
            pass

    print("Network configuration:", wlan.ifconfig())

connect_wifi(ssid, password)



# Camera initialization and functions

def init_camera():
    try:
        camera.init(0, format=camera.JPEG)  # Ajustez les paramètres si nécessaire
        print("Caméra initialisée avec succès")
        return True
    except Exception as e:
        print("Erreur lors de l'initialisation de la caméra:", e)
        return False

def capture_photo():
    try:
        photo = camera.capture()
        print("Photo capturée avec succès")
        time.sleep(1)
        return photo
    except Exception as e:
        print("Erreur lors de la capture de la photo:", e)
        return None

def save_photo(photo, path):
    try:
        with open(path, "wb") as file:
            file.write(photo)
            print(f"Photo sauvegardée à {path}")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde de la photo à {path}: {e}")



flash = machine.Pin(4, machine.Pin.OUT)


def allumer_flash():
    flash.on()

def eteindre_flash():
    flash.off()

def main():
    camera.deinit()
    try:
        if init_camera():
            allumer_flash()  # Turn on the flash
            photo = capture_photo()
            eteindre_flash()  # Turn off the flash

        if photo is not None:
            save_path = "photo.jpg"
            save_photo(photo, save_path)

        camera.deinit()  # Deactivate the camera
    except Exception as camera_error:
        print("Camera error:", camera_error)

    # Read data from BME280 sensor
    bme.doMeasure()
    temperature, pressure, humidity = bme.dumpLastMeasurement()
    print(f"Temperature: {temperature:.2f} C")
    print(f"Pressure: {pressure:.2f} mb")
    print(f"Humidity: {humidity:.2f} %")


if __name__ == "__main__":
    main()
