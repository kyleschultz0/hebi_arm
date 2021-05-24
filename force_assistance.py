from hebi_functions import initialize_hebi, get_hebi_feedback, send_hebi_position_command, send_hebi_effort_command
from encoder_functions import initialize_encoders, get_encoder_feedback
from trajectory_functions import trajectory

import NetFT
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


def save_data(output):
    np.savetxt("csv/PD_1.csv", np.array(output), delimiter=",")
    print("Data saved")

if __name__ == "__main__":
    freq = 100 # Hz
    group, hebi_feedback, command = initialize_hebi()
    group.feedback_frequency = freq
    output = []
    K = np.matrix([[0.1, 0],
                   [0, 0.1]])

    sensor = NetFT.Sensor("192.168.0.11")
    sensor.tare()

    L1 = 0.29
    L2 = 0.22

    i = 0

    while True:

       Fraw = sensor.getForce()
       F = np.array([Fraw[0], 0.9*Fraw[1] + 0.42*Fraw[2]])/1000000.0    # Accounting for y force having z and y components in sensor frame
       # print("Force:", F)
       theta, omega, torque, hebi_limit_stop_flag = get_hebi_feedback(group, hebi_feedback)  
       theta1 = theta[0]
       theta2 = theta[1]
       print("Theta 1:", theta1)
       print("Theta 2:", theta2)

       Jinv = np.matrix([[-np.sin(theta1 + theta2)/(L1*np.cos(theta1 + theta2)*np.sin(theta1) - L1*np.sin(theta1 + theta2)*np.cos(theta1)),
                          -np.cos(theta1 + theta2)/(L1*np.cos(theta1 + theta2)*np.sin(theta1) - L1*np.sin(theta1 + theta2)*np.cos(theta1))],

                         [(L2*np.sin(theta1 + theta2) + L1*np.sin(theta1))/(L1*L2*np.cos(theta1 + theta2)*np.sin(theta1) - L1*L2*np.sin(theta1 + theta2)*np.cos(theta1)),
                          (L2*np.cos(theta1 + theta2) + L1*np.cos(theta1))/(L1*L2*np.cos(theta1 + theta2)*np.sin(theta1) - L1*L2*np.sin(theta1 + theta2)*np.cos(theta1))]])

       #Jinv = np.matrix([[-(100*np.sin(theta1 + theta2))/(27*(np.cos(theta1 + theta2)*np.sin(theta1) - np.sin(theta1 + theta2)*np.cos(theta1))), 
       #                -(100*np.cos(theta1 + theta2))/(27*(np.cos(theta1 + theta2)*np.sin(theta1) - np.sin(theta1 + theta2)*cos(theta1)))],
       #
       #               [(25*(16*np.sin(theta1 + theta2) + 9*np.sin(theta1)))/(108*(np.cos(theta1 + theta2)*np.sin(theta1) - np.sin(theta1 + theta2)*np.cos(theta1))),
       #                (25*(16*np.cos(theta1 + theta2) + 9*np.cos(theta1)))/(108*(np.cos(theta1 + theta2)*np.sin(theta1) - np.sin(theta1 + theta2)*np.cos(theta1)))]])
       # print("Jinv:", Jinv)
       omega_d = Jinv @ K @ F
       omega_d = np.squeeze(np.asarray(omega_d))
       # print("Desired velocities:", omega_d)

       command.velocity = omega_d
       group.send_command(command)

       if i == 0:
           print("Ready to operate...")
           i = 1


       if keyboard.is_pressed('esc'):
           break

