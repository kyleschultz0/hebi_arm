# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 23:35:46 2021

@author: wade9
"""

from hebi_functions import initialize_hebi, get_hebi_feedback, send_hebi_position_command
from encoder_functions import run_encoder_process, read_encoder
from trajectory_functions import initialize_trajectory, trajectory

import csv
import keyboard
import numpy as np
import pandas as pd
from time import time


e_theta = 1


if __name__ == "__main__": 
    group, hebi_feedback, command = initialize_hebi()
    group.feedback_frequency = 50
    arduino = initialize_encoders()
    initialize_trajectory(50)
    t0 = time()
    while True:
        h_theta, h_omega, hf_torque, hebi_limit_stop_flag = get_hebi_feedback(group, hebi_feedback)
        # print('HEBI Omega:', h_omega)
        # print('HEBI Feedback Torque:', hf_torque)
        # print('HEBI Command Torque:', hc_torque)
        e_theta = read_encoder()
        print('HEBI angles:', h_theta)
        print('encoder angles:', e_theta)
        t = time() - t0

        theta = trajectory(t, "combined_trajectories.csv")
        command.position = theta
        send_hebi_position_command(group, command)        
        hc_torque = np.array([0,0]) # no command torque

        try:
            with open('csv/circle_5_15.csv', mode='a') as data_file:
                 data_file = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                 data_file.writerow([t, 
                                     h_theta[0], h_theta[1], 
                                     h_omega[0], h_omega[1], 
                                     hf_torque[0], hf_torque[1],
                                     hc_torque[0], hc_torque[1],
                                     e_theta[0], e_theta[1]])        
        except:
            print("Failed to write to testa data CSV")
        
        if hebi_limit_stop_flag: 
            print("Stopping: HEBI joints past limits")
            break
        if keyboard.is_pressed('q'):
            break
        
        # print('Loop Time:', time()-test_time)
        # test_time=time()