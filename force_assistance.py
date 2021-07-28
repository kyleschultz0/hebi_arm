from hebi_functions import initialize_hebi, get_hebi_feedback, send_hebi_position_command, send_hebi_effort_command
from trajectory_functions import trajectory
from encoder_functions import initialize_encoders, get_encoder_feedback

import NetFT
import keyboard
import numpy as np
from numpy import pi, sin, cos
from time import time, sleep

#=== Global variables ===#

# Initialize force filter:
y1k_1 = 0 # y1[k-1]
f1k_1 = 0 # f1[k-1]
y2k_1 = 0 # y2[k-1]
f2k_1 = 0 # f2[k-1]


def force_filter(force, cutoff_freq, T):
    # input freq in hz
    global y1k_1
    global f1k_1
    global y2k_1
    global f2k_1
    
    tau = 1/(2*pi*cutoff_freq)
    y1 = (force[0] + f1k_1 - (1-2*tau/T)*y1k_1)/(2*tau/T+1)
    y2 = (force[1] + f2k_1 - (1-2*tau/T)*y2k_1)/(2*tau/T+1)
    y1k_1 = y1 
    f1k_1 = force[0]
    y2k_1 = y2
    f2k_1 = force[1]
    return np.array([y1,y2])


def save_data(output):
    np.savetxt("csv/assistance_force.csv", np.array(output), delimiter=",")
    print("Data saved")

if __name__ == "__main__":
    freq = 400 # Hz
    group, hebi_feedback, command = initialize_hebi()
    group.feedback_frequency = freq
    output = []
    K = np.matrix([[1.25, 0],
                   [0, 1.25]])

    Kf = np.matrix([[15, 0],
                  [0, 15]])

    arduino = initialize_encoders()

    group_info = group.request_info()

    if group_info is not None:
        group_info.write_gains("csv/saved_gains.xml")

    sensor = NetFT.Sensor("192.168.0.11")
    sensor.tare()

    #=== Variables for 2 DOF ===#
    L1 = 0.29
    L2 = 0.22
    #======#

    #=== Variables for 3 DOF ===#
    # L1 = 0.268
    # L2 = 0.472
    #======#


    i = 0

    t0 = time()
    t1 = t0 

    while True:

       Fraw = sensor.getForce()
       F = np.array([Fraw[0], - 0.9*Fraw[1] + 0.42*Fraw[2]])/1000000.0    # Accounting for y force having z and y components in sensor frame

       theta_e = get_encoder_feedback(arduino, num_encoders=2)
       theta, omega, torque, hebi_limit_stop_flag = get_hebi_feedback(group, hebi_feedback)  
       theta = theta + np.array([0, np.pi/2])   # offsetting transform
       theta1 = theta[0]
       theta2 = theta[1]
       theta_end = theta1 + theta2 - np.pi/2
       f_adjust = np.array([F[0]*np.cos(theta_end) - F[1]*np.sin(theta_end), F[0]*np.sin(theta_end) + F[1]*np.cos(theta_end)]) 
       T = time() - t1
       t1 = time()
       f_adjust = force_filter(f_adjust, 0.5, T)

       # print("Theta:", theta, theta_e)
        

       Jinv = np.matrix([[cos(theta1 + theta2)/(L1*sin(theta2)), sin(theta1 + theta2)/(L1*sin(theta2))],
                         [-(L2*cos(theta1 + theta2) + L1*cos(theta1))/(L1*L2*sin(theta2)), -(L2*sin(theta1 + theta2) + L1*sin(theta1))/(L1*L2*sin(theta2))]])

       Jt = np.matrix([[- L2*sin(theta1 + theta2) - L1*sin(theta1), L2*cos(theta1 + theta2) + L1*cos(theta1)],
                       [-L2*sin(theta1 + theta2), L2*cos(theta1 + theta2)]])
        
       omega_d = Jinv @ K @ f_adjust
       torque_d = Jt @ Kf @ f_adjust
       print("Before:", omega_d)

       omega_d = np.squeeze(np.asarray(omega_d))
       torque_d = np.squeeze(np.asarray(torque_d))

       print("After:", omega_d)

       # command.velocity = omega_d
       command.effort = torque_d
       group.send_command(command)
       # print("Theta:", theta)

       # Save data
       t = time()-t0
       # output += [[t, theta[0], theta[1] ,theta_e[0], theta_e[1], omega_d[0], omega_d[1], omega[0], omega[1], torque[0], torque[1]]]
       output += [[t, theta[0], theta[1] , torque_d[0], torque_d[1], torque[0], torque[1], f_adjust[0], f_adjust[1]]]

       if i == 0:
           print("Ready to operate...")
           i = 1


       if keyboard.is_pressed('esc'):
           save_data(output)
           break

