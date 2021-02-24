# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 23:35:46 2021

@author: wade9
"""

from hebi_functions import initialize_hebi, get_hebi_feedback, send_hebi_position_command
from encoder_functions import run_encoder_process, read_encoder

import csv
import keyboard
import numpy as np
from time import time


e_theta = 1

def trajectory(t):
    theta = np.array([-np.pi/4*np.sin(np.pi/4*t) + np.pi/2, 
                      np.pi/4*np.sin(np.pi/4*t) + np.pi/2])
    # theta = np.array([np.pi/2, 
    #                   np.pi/2])
    return theta

if __name__ == "__main__": 
    encoder_process = run_encoder_process()
    group, hebi_feedback, command = initialize_hebi()
    group.feedback_frequency = 50
    t = time()
    test_time = time()
    while True:
        h_theta, h_omega, hf_torque, hebi_limit_stop_flag = get_hebi_feedback(group, hebi_feedback)
        e_theta = read_encoder()
        print('HEBI angles:', h_theta)
        print('encoder angles:', e_theta)

        # theta = trajectory(t)
        # command.position = theta
        # send_hebi_position_command(group, command)        
        hc_torque = np.array([0,0]) # no command torque

        # with open('csv/test_data.csv', mode='a') as data_file:
        #     data_file = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        #     data_file.writerow([t, 
        #                         h_theta[0], h_theta[1], 
        #                         h_omega[0], h_omega[1], 
        #                         hf_torque[0], hf_torque[1],
        #                         hc_torque[0], hc_torque[1],
        #                         e_theta[0], e_theta[1]])        
        
        if hebi_limit_stop_flag: 
            print("Stopping: HEBI joints past limits")
            break
        if keyboard.is_pressed('q'):
            break
        
        print('Loop Time:', time()-test_time)
        test_time=time()