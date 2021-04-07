from hebi_functions import initialize_hebi, get_hebi_feedback, send_hebi_position_command, send_hebi_effort_command
from encoder_functions import initialize_encoders, get_encoder_feedback

import keyboard
import numpy as np
from numpy import pi, sin, cos
from time import time

#=== Global variables ===#

# Initialize velocity and acceleration:
theta1k_1 = 0 # theta1[k-1]
theta2k_1 = 0 # theta2[k-1]
omega1k_1 = 0 # omega1[k-1]
omega2k_1 = 0 # omega2[k-1]
alpha1k_1 = 0 # alpha1[k-1]
alpha2k_1 = 0 # alpha2[k-1]

# Initialize velocity filter:
y1k_1 = 0 # y1[k-1]
v1k_1 = 0 # v1[k-1]
y2k_1 = 0 # y2[k-1]
v2k_1 = 0 # v2[k-1]

# Initialize acceleration filter:
z1k_1 = 0 # z1[k-1]
a1k_1 = 0 # a1[k-1]
z2k_1 = 0 # z2[k-1]
a2k_1 = 0 # a2[k-1]

def velocity(theta, T):
    global theta1k_1
    global theta2k_1
    global omega1k_1
    global omega2k_1
    
    omega1 = (2/T)*(theta[0] - theta1k_1) - omega1k_1
    omega2 = (2/T)*(theta[1] - theta2k_1) - omega2k_1
    theta1k_1 = theta[0]
    theta2k_1 = theta[1]
    # replace lines if acceration() is removed, acceleration updates these:
    # omega1k_1 = omega1
    # omega2k_1 = omega2
    return np.array([omega1,omega2])

def velocity_filter(omega, cutoff_freq, T):
    # input freq in hz
    global y1k_1
    global v1k_1
    global y2k_1
    global v2k_1
    
    tau = 1/(2*pi*cutoff_freq)
    y1 = (omega[0] + v1k_1 - (1-2*tau/T)*y1k_1)/(2*tau/T+1)
    y2 = (omega[1] + v2k_1 - (1-2*tau/T)*y2k_1)/(2*tau/T+1)
    y1k_1 = y1 
    v1k_1 = omega[0]
    y2k_1 = y2
    v2k_1 = omega[1]
    return np.array([y1,y2])
    
def acceleration(omega, T):
    global omega1k_1
    global omega2k_1
    global alpha1k_1
    global alpha2k_1
    
    alpha1 = (2/T)*(omega[0] - omega1k_1) - alpha1k_1
    alpha2 = (2/T)*(omega[1] - omega2k_1) - alpha2k_1
    omega1k_1 = omega[0]
    omega2k_1 = omega[1]
    alpha1k_1 = alpha1
    alpha2k_1 = alpha2
    return np.array([alpha1,alpha2])

def acceleration_filter(alpha, cutoff_freq, T):
    # input freq in hz
    global z1k_1
    global a1k_1
    global z2k_1
    global a2k_1
    
    tau = 1/(2*pi*cutoff_freq)
    z1 = (alpha[0] + a1k_1 - (1-2*tau/T)*z1k_1)/(2*tau/T+1)
    z2 = (alpha[1] + a2k_1 - (1-2*tau/T)*z2k_1)/(2*tau/T+1)
    z1k_1 = z1 
    a1k_1 = alpha[0]
    z2k_1 = z2
    a2k_1 = alpha[1]
    return np.array([z1,z2])

def PD_controller(theta,theta_d,omega,omega_d):    
    kp1 = 3.0 # 50hz: 3.0, 200hz: 5.0
    kd1 = 0.5 # 50hz: 0.5, 200hz: 0.5
    kp2 = 1.0 # 50hz: 1.0, 200hz: 3.0
    kd2 = 0.05 # 50hz: 0.05, 200hz: 0.05
    PD_effort = np.array([kp1*(theta_d[0]-theta[0]) + kd1*(omega_d[0]-omega[0]),
                          kp2*(theta_d[1]-theta[1]) + kd2*(omega_d[1]-omega[1])])
    return PD_effort

def trajectory(t, freq=pi):
    theta_d = np.array([pi/2, -pi/2+(pi/4)*sin(freq*t)])
    omega_d = np.array([0, (pi/4)*(freq)*cos(freq*t)])
    alpha_d = np.array([0, -(pi/4)*(freq)**2*sin(freq*t)])
    return theta_d, omega_d, alpha_d

def save_data(output):
    np.savetxt("csv/PD_1.csv", np.array(output), delimiter=",")
    print("Data saved")

if __name__ == "__main__":
    T = 0.02
    group, hebi_feedback, command = initialize_hebi()
    group.feedback_frequency = 1/T
    arduino = initialize_encoders()
    
    t0 = time()
    output = []
    
    while True:
        t = time()-t0
        h_theta, h_omega, hf_torque, hebi_limit_stop_flag = get_hebi_feedback(group, hebi_feedback)       
        theta = get_encoder_feedback(arduino)
        omega = velocity(theta, T)
        omega = velocity_filter(omega, 2, T)
        alpha = acceleration(omega, T)
        alpha = acceleration_filter(alpha, 2, T)
                       
        theta_d, omega_d, alpha_d = trajectory(t)
        
        effort = PD_controller(theta,theta_d,omega,omega_d)
        command.effort = effort
        send_hebi_effort_command(group, command)
        
        output += [[t,h_theta[0],theta[0],effort[0]]]
        
        if hebi_limit_stop_flag: 
            save_data(output)
            print("Stopping: HEBI joints past limits")
            break
        if keyboard.is_pressed('esc'):
            save_data(output)
            print("Stopping: User input stop command")
            break
        if t > 10:
            save_data(output)
            print("Stopping: Time limit reached")
            break