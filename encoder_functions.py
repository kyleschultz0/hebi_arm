# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 11:24:10 2021

@author: wade9
"""
import serial
import numpy as np
import time
   
def decode_readings(readings, num_encoders):
    output = np.zeros(num_encoders)
    
    for reading in readings:
        try:
            string_list = reading.decode("utf-8").split(",")
            index = int(string_list[0]) - 1
            output[index] = float(string_list[2])*(np.pi/180)
        except:
            print("error decoding")
    return output

def get_encoder_feedback(arduino, num_encoders=2, joint_offsets=np.array([3.069, 3.574]), limit_stop=True, limits=np.array([7*np.pi/6, 11*np.pi/6])):
    # joint_offsets - set in radians to change x/y position
    # limit_stop currently limits position of both joints the same [lower limit, higher limit] in radians
    limit_stop_flag = False
    readings = []
    
    for i in range(num_encoders):
        # arduino.reset_input_buffer()
        reading = arduino.readline()
        # print(reading)
        readings += [reading]
    theta = np.array(decode_readings(readings, num_encoders=num_encoders))
    theta -= joint_offsets
    if (theta > limits).any():
        limit_stop_flag = True
    return theta, limit_stop_flag
    
def initialize_encoders(com='COM3', baudrate=115200):
    arduino = serial.Serial(com,baudrate)
    return arduino

# to test functions:
if __name__ == "__main__":
    arduino = initialize_encoders()
    print("Start of data")
    while True:
        get_encoder_feedback(arduino, num_encoders=2)
        
    