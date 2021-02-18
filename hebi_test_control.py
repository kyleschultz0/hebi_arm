# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 23:35:46 2021

@author: wade9
"""

import hebi
from hebi_functions import initialize_hebi, get_hebi_feedback, send_hebi_command
from encoder_functions import initialize_encoders, get_encoder_feedback

import keyboard
import numpy as np
from time import time

def trajectory(t):
    theta = np.array([np.pi/4*np.cos(np.pi/2*t) + np.pi/2, 
                      np.pi/4*np.sin(np.pi/2*t) + np.pi/2])
    return theta

if __name__ == "__main__":
    group, hebi_feedback, command = initialize_hebi()
    group.feedback_frequency=50
    arduino = initialize_encoders()
    
    t0 = time()
    h_theta, h_omega, h_torque, hebi_limit_stop_flag = get_hebi_feedback(group, hebi_feedback)
    while True:
        # time2 = time()
        e_theta, encoder_limit_stop_flag = get_encoder_feedback(arduino)
        # print('Encoder time: ', time2 - time())
        
        ### code here ###
        
        # command.position = np.array([np.pi/2, np.pi/2])
        # theta = trajectory(time())
        # command.position = theta
        # send_hebi_command(group, command)
        
        print('HEBI angles:', h_theta)
        print('encoder angles:', e_theta)
        
        #################
        
        #if hebi_limit_stop_flag: 
         #   print("Stopping: HEBI joints past limits")
          #  break
        #if encoder_limit_stop_flag: 
         #   print("Stopping: encoder joints past limits")
          #  break
        if keyboard.is_pressed('q'):
            break
        
        h_theta, h_omega, h_torque, hebi_limit_stop_flag = get_hebi_feedback(group, hebi_feedback)
        print('Time after feedback:', time()-t0)
        t0 = time()