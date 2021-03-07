import csv
import serial
import numpy as np
from time import time, sleep
from multiprocessing import Process

encoder_backup_theta = np.array([0,0])

def initialize_encoders(com='COM3', baudrate=115200, timeout=1, num_init_loops=5):
    arduino = serial.Serial(com,baudrate,timeout=timeout)
    sleep(0.1)
    arduino.reset_input_buffer()
    for i in range(num_init_loops):
        try:
            get_reading(arduino)
        except:
            pass
    return arduino
   
def decode_readings(readings, num_encoders):
    output = np.zeros(num_encoders)
    for reading in readings:
        string_list = reading.decode("utf-8").split(",")
        index = int(string_list[0]) - 1
        output[index] = float(string_list[1])*(2*np.pi/4096)
    return output

def get_reading(arduino):
    reading = 'empty_reading'
    while reading == 'empty_reading':
        arduino.write(b'b')
        reading = arduino.readline()
    return reading

def get_encoder_feedback(arduino, num_encoders=2, joint_offsets=np.array([3.519, 3.11])):
    # joint_offsets - set in radians to change x/y position
    readings = []
    for i in range(num_encoders):
        reading = get_reading(arduino)
        readings += [reading]
    theta = decode_readings(readings, num_encoders=num_encoders)
    theta -= joint_offsets
    return theta
    
# to test functions:
if __name__ == "__main__":
    arduino = initialize_encoders()
    while True:
        t0 = time()
        theta = get_encoder_feedback(arduino, num_encoders=2)
        print(theta)
        print('Encoder Feedback Time:', time()-t0)