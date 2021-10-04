from hebi_functions import initialize_hebi, get_hebi_feedback, send_hebi_position_command, send_hebi_effort_command
from trajectory_functions import trajectory
from encoder_functions import initialize_encoders, get_encoder_feedback
from controller_input import initialize_joystick, get_axis


import keyboard
import numpy as np
from numpy import pi, sin, cos
from time import time, sleep

#=== Global variables ===#

# Initialize input filter:
y1k_1 = 0 # y1[k-1]
f1k_1 = 0 # f1[k-1]
y2k_1 = 0 # y2[k-1]
f2k_1 = 0 # f2[k-1]


def input_filter(input, cutoff_freq, T):
    # input freq in hz
    global y1k_1
    global f1k_1
    global y2k_1
    global f2k_1
    
    tau = 1/(2*pi*cutoff_freq)
    y1 = (input[0] + f1k_1 - (1-2*tau/T)*y1k_1)/(2*tau/T+1)
    y2 = (input[1] + f2k_1 - (1-2*tau/T)*y2k_1)/(2*tau/T+1)
    y1k_1 = y1 
    f1k_1 = input[0]
    y2k_1 = y2
    f2k_1 = input[1]
    return np.array([y1,y2])


def save_data(output):
    np.savetxt("csv/controller1.csv", np.array(output), delimiter=",")
    print("Data saved")

def controller_operation(joystick, group, hebi_feedback, command, L1, L2, T):
    K = np.matrix([[0.25, 0],
                   [0, 0.25]])
    axis = get_axis(joystick)
    axis_f = input_filter(axis, 10, T)
    axis_f = np.squeeze(np.asarray(axis_f))
    theta, omega, torque, hebi_limit_stop_flag = get_hebi_feedback(group, hebi_feedback)
    theta1 = theta[0]
    theta2 = theta[1]
    Jinv = np.matrix([[cos(theta1 + theta2)/(L1*sin(theta2)), sin(theta1 + theta2)/(L1*sin(theta2))],
                      [-(L2*cos(theta1 + theta2) + L1*cos(theta1))/(L1*L2*sin(theta2)), -(L2*sin(theta1 + theta2) + L1*sin(theta1))/(L1*L2*sin(theta2))]])
    omega_d = Jinv @ K @ axis_f
    omega_d = np.squeeze(np.asarray(omega_d))
    command.velocity = omega_d
    group.send_command(command)



#if __name__ == "__main__":
#    freq = 100 # Hz
#    group, hebi_feedback, command = initialize_hebi()
#    group.feedback_frequency = freq
#    arduino = initialize_encoders()
#    group_info = group.request_info()
#    joystick = initialize_joystick()


#    if group_info is not None:
#        group_info.write_gains("csv/saved_gains.xml")



#    #=== Variables for 2 DOF ===#
#    L1 = 0.29
#    L2 = 0.22
#    #======#

#    #=== Variables for 3 DOF ===#
#    # L1 = 0.268
#    # L2 = 0.472
#    #======#


#    i = 0

#    t0 = time()
#    t1 = t0 
#    sleep(0.001)

#    while True:

#       T = time() - t1
#       t1 = time()
#       controller_operation(joystick, group, hebi_feedback, command, L1, L2, T)


#       if i == 0:
#           print("Ready to operate...")
#           i = 1


#       if keyboard.is_pressed('esc'):
#           break



if __name__ == "__main__":
    freq = 400 # hz
    group, hebi_feedback, command = initialize_hebi()
    group.feedback_frequency = freq
    joystick = initialize_joystick()
    output = []
    k = np.matrix([[0.25, 0],
                   [0, 0.25]])

    kf = np.matrix([[15, 0],
                  [0, 15]])

    arduino = initialize_encoders()

    group_info = group.request_info()

    if group_info is not None:
        group_info.write_gains("csv/saved_gains.xml")



    #=== variables for 2 dof ===#
    l1 = 0.29
    l2 = 0.22
    #======#

    #=== variables for 3 dof ===#
    # l1 = 0.268
    # l2 = 0.472
    #======#


    i = 0

    t0 = time()
    t1 = t0 

    while True:

       axis = get_axis(joystick)

       theta_e = get_encoder_feedback(arduino, num_encoders=2)
       theta, omega, torque, hebi_limit_stop_flag = get_hebi_feedback(group, hebi_feedback)  
       theta = theta + np.array([0, np.pi/2])   # offsetting transform
       theta1 = theta[0]
       theta2 = theta[1]
       t = time() - t1
       t1 = time()
       print(axis)
       axis_f = input_filter(axis, 10, t)

        

       jinv = np.matrix([[cos(theta1 + theta2)/(l1*sin(theta2)), sin(theta1 + theta2)/(l1*sin(theta2))],
                         [-(l2*cos(theta1 + theta2) + l1*cos(theta1))/(l1*l2*sin(theta2)), -(l2*sin(theta1 + theta2) + l1*sin(theta1))/(l1*l2*sin(theta2))]])

       jt = np.matrix([[- l2*sin(theta1 + theta2) - l1*sin(theta1), l2*cos(theta1 + theta2) + l1*cos(theta1)],
                       [-l2*sin(theta1 + theta2), l2*cos(theta1 + theta2)]])
        
       omega_d = jinv @ k @ axis_f
       # torque_d = jt @ kf @ axis_f

       omega_d = np.squeeze(np.asarray(omega_d))
       # torque_d = np.squeeze(np.asarray(torque_d))
       # print("omega desired:", omega_d, "\n")

       command.velocity = omega_d
       # command.effort = torque_d
       # group.send_command(command)
       t = time() - t0
       output += [[t, theta[0], theta[1] , omega_d[0], omega_d[1], omega[0], omega[1], axis[0], axis[1], axis_f[0], axis_f[1]]]

       if i == 0:
           print("ready to operate...")
           i = 1


       if keyboard.is_pressed('esc'):
           save_data(output)
           break


