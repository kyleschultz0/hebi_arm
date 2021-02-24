# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 11:24:10 2021

@author: wade9
"""
import csv
import serial
import numpy as np
from time import time, sleep
from multiprocessing import Process

encoder_backup_theta = np.array([0,0])

def initialize_encoders(com='COM3', baudrate=115200):
    arduino = serial.Serial(com,baudrate)
    sleep(0.1)
    arduino.reset_input_buffer()
    try:
        arduino.readline()
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

def get_encoder_feedback(arduino, num_encoders=2, joint_offsets=np.array([3.069, 3.574])):
    # joint_offsets - set in radians to change x/y position
    readings = []
    for i in range(num_encoders):
        reading = arduino.readline()
        readings += [reading]
    theta = decode_readings(readings, num_encoders=num_encoders)
    theta -= joint_offsets
    
    try:
        with open('csv/encoder.csv', mode='w') as data_file:
            data_file = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            data_file.writerow([theta[0], theta[1]])
    except:
        pass
    return

def encoder_process():
    arduino = initialize_encoders()
    while True:
        get_encoder_feedback(arduino)
    return

def run_encoder_process():
    proc = Process(target=encoder_process)
    proc.start()
    return proc

def read_encoder():
    global encoder_backup_theta
    try:
        with open('csv/encoder.csv', mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')  
            for row in csv_reader:
                theta = np.array([float(row[0]), float(row[1])])
                encoder_backup_theta = theta
                return 
                break
    except:
        print('HY')
        return encoder_backup_theta
    
# to test functions:
if __name__ == "__main__":
    arduino = initialize_encoders()
    while True:
        t0 = time()
        theta = get_encoder_feedback(arduino, num_encoders=2)
        print(theta)
        print('Encoder Feedback Time:', time()-t0)
    