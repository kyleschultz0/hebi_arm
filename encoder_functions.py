import serial
import numpy as np
from time import time, sleep

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
   
def decode_reading(reading, num_encoders):
    encoder_output = np.zeros(num_encoders)
    string_list = reading.decode("utf-8").split(",")
    encoder_output[0] = float(string_list[0])*(2*np.pi/4096)
    encoder_output[1] = float(string_list[1])*(2*np.pi/4096)
    return encoder_output

def get_reading(arduino):
    reading = 'empty_reading'
    while reading == 'empty_reading':
        arduino.write(b'b') # send any byte to call reading, sending 'b'
        reading = arduino.readline()
    return reading

def get_encoder_feedback(arduino, num_encoders=2, joint_offsets=np.array([3.528, 1.5])):
    # joint_offsets - set in radians to change x/y position
    reading = get_reading(arduino)
    theta = decode_reading(reading, num_encoders=num_encoders)
    theta -= joint_offsets
    theta += np.array([-np.pi, -np.pi])
    theta *= -1
    return theta
    
# to test functions:
if __name__ == "__main__":
    arduino = initialize_encoders()
    while True:
        t0 = time()
        theta = get_encoder_feedback(arduino, num_encoders=2)
        print(theta)
        print('Encoder Feedback Time:', time()-t0)