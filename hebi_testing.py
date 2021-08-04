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



if __name__ == "__main__": 
    group, hebi_feedback, command = initialize_hebi()
    group.feedback_frequency = 100
    traj = initialize_trajectory("csv/trajectories_4sin01.csv")
    t0 = time()
    log_file_location = group.start_log("C:/Users/Student/Source/Repos/hebi_arm/csv", 'force_4sin01_nocables.hebilog')

    while True:

        theta, omega, torque, hebi_limit_stop_flag = get_hebi_feedback(group, hebi_feedback)
        t = time() - t0

        torque_d = trajectory(t, traj)
        command.effort = torque_d
        group.send_command(command)  

        
        if hebi_limit_stop_flag: 
            print("Stopping: HEBI joints past limits")
            break

        if keyboard.is_pressed('esc'):
            save_data(output)
            group.stop_log()
            break
