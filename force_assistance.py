from hebi_functions import initialize_hebi, get_hebi_feedback, send_hebi_position_command, send_hebi_effort_command
from trajectory_functions import trajectory

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

t_1 = 0


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
    

def PD_controller(theta,theta_d,omega,omega_d):    
    kp1 = 10.0 # 50hz: 3.0, 200hz: 5.0
    kd1 = 0.2 # 50hz: 0.5, 200hz: 0.5
    kp2 = 10.0 # 50hz: 1.0, 200hz: 3.0
    kd2 = 0.1 # 50hz: 0.05, 200hz: 0.05
    PD_effort = np.array([kp1*(theta_d[0]-theta[0]) + kd1*(omega_d[0]-omega[0]),
                          kp2*(theta_d[1]-theta[1]) + kd2*(omega_d[1]-omega[1])])
    return PD_effort


def save_data(output):
    np.savetxt("csv/assistance_500hz.csv", np.array(output), delimiter=",")
    print("Data saved")

def loop_timer(t0, T, print_loop_time=False):
    global t_1
    t = time()-t0
    while (t - t_1) < T:
        t = time()-t0
    if print_loop_time:
        print('Loop Time:', round(t-t_1, 8), 'seconds')
    t_1 = t
    return t

if __name__ == "__main__":
    freq = 0 # Hz
    group, hebi_feedback, command = initialize_hebi()
    group.feedback_frequency = freq
    output = []
    K = np.matrix([[0.75, 0],
                   [0, 0.75]])

    group_info = group.request_info()

    if group_info is not None:
        group_info.write_gains("gains/saved_gains.xml")

    sensor = NetFT.Sensor("192.168.0.11")
    sensor.tare()

    L1 = 0.29
    L2 = 0.22

    i = 0

    freq = 500
    T = 1/freq
    t0 = time()
    while True:

       t = loop_timer(t0, T, print_loop_time=False)
       Fraw = sensor.getForce()
       F = np.array([Fraw[0], - 0.9*Fraw[1] + 0.42*Fraw[2]])/1000000.0    # Accounting for y force having z and y components in sensor frame

       theta, omega, torque, hebi_limit_stop_flag = get_hebi_feedback(group, hebi_feedback)  
       theta1 = theta[0]
       theta2 = theta[1]
       theta_end = theta1 + theta2 - np.pi/2
       f_adjust = np.array([F[0]*np.cos(theta_end) - F[1]*np.sin(theta_end), F[0]*np.sin(theta_end) + F[1]*np.cos(theta_end)]) 
       f_adjust = force_filter(f_adjust, 0.3, T)
        

       Jinv = np.matrix([[cos(theta1 + theta2)/(L1*sin(theta2)), sin(theta1 + theta2)/(L1*sin(theta2))],
                         [-(L2*cos(theta1 + theta2) + L1*cos(theta1))/(L1*L2*sin(theta2)), -(L2*sin(theta1 + theta2) + L1*sin(theta1))/(L1*L2*sin(theta2))]])

       omega_d = Jinv @ K @ f_adjust
       omega_d = np.squeeze(np.asarray(omega_d))

       command.velocity = omega_d
       group.send_command(command)

       # Save data for troubleshooting
       h_theta, h_omega, hf_torque, hebi_limit_stop_flag = get_hebi_feedback(group, hebi_feedback)
       t = time()-t0
       output += [[t, f_adjust[0], f_adjust[1], Fraw[0], Fraw[1], theta[0], theta[1], omega_d[0], omega_d[1], h_omega[0], h_omega[1]]]
       # print(output)

       if i == 0:
           print("Ready to operate...")
           i = 1


       if keyboard.is_pressed('esc'):
           save_data(output)
           break

