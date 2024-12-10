"""
The Python code you will write for this module should read
acceleration data from the IMU. When a reading comes in that surpasses
an acceleration threshold (indicating a shake), your Pi should pause,
trigger the camera to take a picture, then save the image with a
descriptive filename. You may use GitHub to upload your images automatically,
but for this activity it is not required.

The provided functions are only for reference, you do not need to use them. 
You will need to complete the take_photo() function and configure the VARIABLES section
"""

#AUTHOR: 
#DATE:

#import libraries
import time
import board
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL
from git import Repo
from picamera2 import Picamera2, Preview
import math

#VARIABLES
NAME = "CalvinM"
THRESHOLD = 4          #Any desired value from the accelerometer
FOLDER_PATH = "output" #Your image folder path in your GitHub repo: ex. /Images

#imu and camera initialization
i2c = board.I2C()
accel_gyro = LSM6DS(i2c)
mag = LIS3MDL(i2c)
picam2 = Picamera2()

def img_gen(name):
    """
    This function is complete. Generates a new image name.

    Parameters:
        name (str): your name ex. MasonM
    """
    t = time.strftime("_%H%M%S")
    imgname = (f'{FOLDER_PATH}/{name}{t}.jpg')
    return imgname

def take_photo():
    """
    This function is NOT complete. Takes a photo when the FlatSat is shaken.
    Replace psuedocode with your own code.
    """
    # configure picamera2 to take photos at the size of the sensor
    mode = picam2.sensor_modes[2]
    camera_config = picam2.create_still_configuration(sensor={"output_size": mode['size'], "bit_depth": mode['bit_depth']})
    picam2.configure(camera_config)
    picam2.start()
    print("SENSOR MODES", picam2.sensor_modes)
    print("CAMERA CONFIG", camera_config)

    last_time = time.time()
    while True:
        accelx, accely, accelz = accel_gyro.acceleration
        
        # calculate magnitude of acceleration
        length_squared = accelx*accelx + accely * accely + accelz * accelz 
        length = math.sqrt(length_squared)
        length -= 9.83
        length = max(length, 0)

        # only allow taking photos more than 1 second after last photo
        delay = time.time() - last_time
        
        if (delay > 1):
            if (length >= THRESHOLD):
                picam2.capture_file(img_gen(NAME))
                print(f"AAAAAAAAAUUUUUUUUUUGHHHHHHHHHHHHH STOP THROWING ME {length:.2f}")
                last_time = time.time()

def main():
    take_photo()

if __name__ == '__main__':
    main()
