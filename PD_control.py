from hebi_functions import initialize_hebi, get_hebi_feedback, send_hebi_position_command, send_hebi_effort_command
from encoder_functions import initialize_encoders, get_encoder_feedback
from trajectory_functions import trajectory

import keyboard
import numpy as np
from numpy import pi, sin, cos
from time import time, sleep

#=== Global variables ===#

# Initialize velocity and acceleration:
theta1k_1 = 0 # theta1[k-1]
theta2k_1 = 0 # theta2[k-1]
omega1k_1 = 0 # omega1[k-1]
omega2k_1 = 0 # omega2[k-1]

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
    
    omega1 = (1/T)*(theta[0] - theta1k_1)
    omega2 = (1/T)*(theta[1] - theta2k_1)
    theta1k_1 = theta[0]
    theta2k_1 = theta[1]
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
    
    alpha1 = (1/T)*(omega[0] - omega1k_1)
    alpha2 = (1/T)*(omega[1] - omega2k_1)
    omega1k_1 = omega[0]
    omega2k_1 = omega[1]

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
    kp1 = 10.0 # 50hz: 3.0, 200hz: 5.0
    kd1 = 0.2 # 50hz: 0.5, 200hz: 0.5
    kp2 = 10.0 # 50hz: 1.0, 200hz: 3.0
    kd2 = 0.1 # 50hz: 0.05, 200hz: 0.05
    PD_effort = np.array([kp1*(theta_d[0]-theta[0]) + kd1*(omega_d[0]-omega[0]),
                          kp2*(theta_d[1]-theta[1]) + kd2*(omega_d[1]-omega[1])])
    return PD_effort

#def trajectory(t, freq=pi, mag=pi/4):
#    # both links sinusoidal:
#    theta_d = np.array([(mag)*sin(freq*t - pi/2) + pi/2, (mag)*sin(freq*t)])
#    omega_d = np.array([(mag)*(freq)*cos(freq*t - pi/2), (mag)*(freq)*cos(freq*t)])
#    alpha_d = np.array([-(mag)*(freq)**2*sin(freq*t - pi/2), -(mag)*(freq)**2*sin(freq*t)])
    
#    # link 2 sinusoidal:
#    # theta_d = np.array([pi/2, (mag)*sin(freq*t)])
#    # omega_d = np.array([0, (mag)*(freq)*cos(freq*t)])
#    # alpha_d = np.array([0, -(mag)*(freq)**2*sin(freq*t)])
    
#    # link 1 sinusoidal:
#    # theta_d = np.array([(mag)*sin(freq*t - pi/2) + pi/2,     0])
#    # omega_d = np.array([(mag)*(freq)*cos(freq*t - pi/2),     0])
#    # alpha_d = np.array([-(mag)*(freq)**2*sin(freq*t - pi/2), 0])
    
#    # link 2 linear (WARNING: UNSTABLE):
#    # theta_d = np.array([pi/2, mag*t - pi/2])
#    # omega_d = np.array([0, mag])
#    # alpha_d = np.array([0, 0])
#    return theta_d, omega_d, alpha_d

def save_data(output):
    np.savetxt("csv/PD_1.csv", np.array(output), delimiter=",")
    print("Data saved")

if __name__ == "__main__":
    freq = 50 # Hz
    group, hebi_feedback, command = initialize_hebi()
    group.feedback_frequency = freq
    arduino = initialize_encoders()
    
    t0 = time()
    t_1 = t0
    sleep(0.001)

    output = []
    while True:
        t = time() - t0
        T = time() - t_1
        t_1 = time()
        
        h_theta, h_omega, hf_torque, hebi_limit_stop_flag = get_hebi_feedback(group, hebi_feedback)       
        theta = get_encoder_feedback(arduino)
        omega = velocity(theta, T)
        omega = velocity_filter(omega, 5, T)
                       
        t, theta_d, omega_d = trajectory(t, "trajectories/cstar_10_20.csv")

        t_2 = time() - t_1
        print("Loop time:", t_2)
        
        effort = PD_controller(theta,theta_d,omega,omega_d)
        command.effort = effort
        send_hebi_effort_command(group, command)
        
        output += [[t,theta_d[0],theta[0],h_theta[0],omega[0],effort[0],
                      theta_d[1],theta[1],h_theta[1],omega[1],effort[1]]]
        
        if hebi_limit_stop_flag: 
            save_data(output)
            print("Stopping: HEBI joints past limits")
            break
        if keyboard.is_pressed('esc'):
            save_data(output)
            print("Stopping: User input stop command")
            break
        if t > 20:
            save_data(output)
            print("Stopping: Time limit reached")
            break