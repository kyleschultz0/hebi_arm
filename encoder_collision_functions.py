import serial
import numpy as np
from time import time, sleep
import keyboard

class Encoder:
    def __init__(self,num_encoders,com=['COM4'], baudrate=115200, timeout=1, num_init_loops=5, joint_offsets=None):
        '''
        Obejct builder
        '''
        self.num_encoders=num_encoders
        if joint_offsets:
            self.joint_offsets=joint_offsets
        else:
            self.joint_offsets=np.zeros(num_encoders*len(com))
           
        self.initialize_encoders(com,baudrate,timeout,num_init_loops)

    def initialize_encoders(self,com,baudrate,timeout, num_init_loops):
        '''
        Initialize connection to arduinos
        '''
        print("Beginnining Initialization")
        self.arduinos=[]
        for port in com:
            self.arduinos.append(serial.Serial(port,baudrate,timeout=timeout))
            sleep(0.1)
       
        for arduino in self.arduinos:
            arduino.reset_input_buffer()
           
        for i in range(num_init_loops):
            try:
                self.get_reading()
            except:
                print("Error Initializing... Retrying")
                pass
        print("Initialized")
       
    def decode_reading(self, readings):
        '''
        parse strings from arduino
        '''
        encoder_outputs = np.zeros((len(self.arduinos), self.num_encoders))
        string_lists=[]
        for reading in readings:
            print("Reading =", reading)
            string_lists.append(reading.decode("utf-8").split(","))
       
        for j,string_list in enumerate(string_lists):
            for i in range(self.num_encoders):
                encoder_outputs[j,i] = float(string_list[i])*(2*np.pi/4096)  # Input
               
        encoder_outputs = np.reshape(encoder_outputs,(-1))
        return encoder_outputs
   
    def get_reading(self):
        '''
        query encoder readings from arduinos
        '''
        readings=[None for _ in self.arduinos]
        for i,arduino in enumerate(self.arduinos):
            while readings[i]:
                arduino.write(b'b') # send any byte to call reading, sending 'b'
                readings[i]=arduino.readline()

        return readings
   
    def get_encoder_feedback(self):
        '''
        get joint angles from encoder
        '''
        # joint_offsets - set in radians to change x/y position
        readings= self.get_reading()
        theta = self.decode_reading(readings)
        theta -= self.joint_offsets
        theta *= -1
        return theta
   
    def save_data(output):
        '''
        save data to csv
        '''
        np.savetxt("csv/EncoderTest_dynamic.csv", np.array(output), delimiter=",")
        print("Data saved")
   
# to test functions:
if __name__ == "__main__":
    encoder = Encoder(num_encoders=3)
    print("Initialization complete!")
    output = []
    t0 = time()
    while True:
        theta = encoder.get_encoder_feedback()
        print(theta)
        t = time()-t0
        output += [[t,theta[0],theta[1]]]

        if keyboard.is_pressed('esc'):
            encoder.save_data(output)
            print("Stopping: User input stop command")
            break
