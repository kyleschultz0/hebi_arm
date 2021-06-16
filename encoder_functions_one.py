import serial
import numpy as np
from time import time, sleep
import keyboard

def initialize_encoders(com1='COM4', com2='COM3', baudrate=115200, timeout=1, num_init_loops=5):
    print("Beginnining Initialization")
    arduino1 = serial.Serial(com1,baudrate,timeout=timeout)
    sleep(0.1)
    arduino2 = serial.Serial(com2,baudrate,timeout=timeout)
    sleep(0.1)
    arduino1.reset_input_buffer()
    arduino2.reset_input_buffer()
    for i in range(num_init_loops):
        try:
            get_reading(arduino1, arduino2)
        except:
            print("Error Initializing... Retrying")
            pass
    print("Initialized")
    return arduino1, arduino2
   
def decode_reading(reading1, reading2, num_encoders):
    encoder_output1 = np.zeros(num_encoders)
    encoder_output2 = np.zeros(num_encoders)
    string_list1 = reading1.decode("utf-8").split(",")
    string_list2 = reading2.decode("utf-8").split(",")
    for i in range(num_encoders):
        encoder_output1[i] = float(string_list1[i])*(2*np.pi/4096)  # Input
        encoder_output2[i] = float(string_list2[i])*(2*np.pi/4096)  # In-tank
    encoder_output = np.concatenate([encoder_output1,encoder_output2])
    return encoder_output

def get_reading(arduino1, arduino2):
    reading1 = 'empty_reading'
    while reading1 == 'empty_reading':
        arduino1.write(b'b') # send any byte to call reading, sending 'b'
        reading1 = arduino1.readline()
        arduino2.write(b'b')
        reading2 = arduino2.readline()
    return reading1, reading2

def get_encoder_feedback(arduino1, arduino2, num_encoders, joint_offsets=np.array([0, 0])):
    # joint_offsets - set in radians to change x/y position
    reading1, reading2 = get_reading(arduino1, arduino2)
    theta = decode_reading(reading1, reading2, num_encoders=num_encoders)
    theta -= joint_offsets
    theta *= -1
    return theta

def save_data(output):
    np.savetxt("csv/EncoderTest_dynamic.csv", np.array(output), delimiter=",")
    print("Data saved")
    
# to test functions:
if __name__ == "__main__":
    arduino1, arduino2 = initialize_encoders()
    print("Initialization complete!")
    output = []
    t0 = time()
    while True:
        theta = get_encoder_feedback(arduino1, arduino2, num_encoders=1)
        print(theta)
        t = time()-t0
        output += [[t,theta[0],theta[1]]]

        if keyboard.is_pressed('esc'):
            save_data(output)
            print("Stopping: User input stop command")
            break

        #if t > 20:
        #    save_data(output)
        #    print("Stopping: Time limit reached")
        #    break