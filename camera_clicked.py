import RPi.GPIO as GPIO
import time
from picamera import PiCamera
import os
import pyrebase

# Firebase configuration
firebaseConfig = {
    "apiKey": "AIzaSyC_44sTT4cGsd9yGMhm9YU4TzSq7zE3CdM",
    "authDomain": "glassist-c0be2.firebaseapp.com",
    "databaseURL": "https://glassist-c0be2-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "glassist-c0be2",
    "storageBucket": "glassist-c0be2.appspot.com",
    "messagingSenderId": "60531876998",
    "appId": "1:60531876998:web:20532f6e661c38a89b9d07",
    "measurementId": "G-G8NFVNPVNX"
}
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
storage = firebase.storage()

# Camera configuration
# camera = PiCamera()
# camera.resolution = (640, 480)

# test simple_clicked
def simple_clicked():
    print("Kiri mau ke click")

# Callback function everytime it's clicked
def button_callback():
    print("Camera clicked!")
    camera.start_preview()
    time.sleep(0.5)

    num = len(os.listdir(os.path.join(os.getcwd(), 'dataset_img')))
    img_name = "dataset_img/dataset_{}.jpg".format(num)
    camera.capture(img_name)

    # Send the data to firebase
    ## Send the status data
    data = {"number of files": str(num), "upload": "success"}
    print(db.child("metadata").set(data))

    ## Send the image
    print(storage.child(img_name).put(img_name))

pin_raspi = 18 # Number of the pin that switch use
pin_raspi_kiri = 17
def setup_raspi(pin_number):
    GPIO.setmode(GPIO.BCM) # Use physical pin number
    GPIO.setup(pin_number, GPIO.IN, pull_up_down=GPIO.PUD_UP) # set the pin according to

# Setup the raspi
setup_raspi(pin_raspi)
setup_raspi(pin_raspi_kiri)

while True:
    try:
        input_state = GPIO.input(pin_raspi)
        if input_state == False:
            # button_callback()
            print("kanan")
            time.sleep(0.5)
        kiri_state = GPIO.input(pin_raspi_kiri)
        if kiri_state == False:
            simple_clicked()
            time.sleep(0.5)
    except Exception as e:
        print(e)
        break
