# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 23:35:46 2021

@author: wade9
"""

from hebi_functions import initialize_hebi, get_hebi_feedback, send_hebi_position_command
from encoder_functions import initialize_encoders, get_encoder_feedback
from trajectory_functions import initialize_trajectory, trajectory

import csv
import keyboard
import numpy as np
import pandas as pd
from time import time
import os

def save_data(output):
    np.savetxt("csv/weights_test.csv", np.array(output), delimiter=",")
    print("Data saved")



e_theta = 1


if __name__ == "__main__": 
    group, hebi_feedback, command = initialize_hebi()
    group.feedback_frequency = 100
    arduino = initialize_encoders()
    traj = initialize_trajectory("csv/trajectories_sin01.csv")
    t0 = time()
    theta_d = np.array([0, 0])
    output = []
    log_file_location = group.start_log("C:/Users/Student/Source/Repos/hebi_arm/csv", 'weights_test')

    while True:

        theta_e = get_encoder_feedback(arduino, num_encoders=2)
        theta, omega, torque, hebi_limit_stop_flag = get_hebi_feedback(group, hebi_feedback)
        t = time() - t0

        theta_d = trajectory(t, traj)
        theta_d = np.array([np.pi/4, -np.pi/4])
        command.effort = np.array([0, -3])
        # command.position = theta_d
        group.send_command(command)(group, command)        
        # hc_torque = np.array([0,0]) # no command torque

        t = time()-t0
        output += [[t, theta[0], theta[1] ,theta_e[0], theta_e[1], theta_d[0], theta_d[1], omega[0], omega[1], torque[0], torque[1]]]
        
        if hebi_limit_stop_flag: 
            print("Stopping: HEBI joints past limits")
            break

        if keyboard.is_pressed('esc'):
            # save_data(output)
            group.stop_log()
            break
        
        # print('Loop Time:', time()-test_time)
        # test_time=time()