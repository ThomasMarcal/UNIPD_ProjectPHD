import camera
import os
import time
import machine 

def init_camera():
    try:
        camera.init(0, format=camera.JPEG)
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
            print("Photo sauvegardée à ", {path})
    except Exception as e:
        print("Erreur lors de la sauvegarde de la photo à {path}:", e)


def allumer_flash():
    flash = machine.Pin(4, machine.Pin.OUT)
    flash.on()

def eteindre_flash():
    flash = machine.Pin(4, machine.Pin.OUT)
    flash.off()

def main():
    camera.deinit() 
    if init_camera():
        allumer_flash()
        photo = capture_photo()
        eteindre_flash()

        if photo is not None:
            save_path = "photo.jpg"
            save_photo(photo, save_path)

        camera.deinit()
        
if __name__ == "__main__":
    main()

