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
    Jinv = np.matrix([[-cos(theta1 + theta2)/(L1*cos(theta2)), -sin(theta1 + theta2)/(L1*cos(theta2))],
                      [(L2*cos(theta1 + theta2) + L1*sin(theta1))/(L1*L2*cos(theta2)), (L2*sin(theta1 + theta2) - L1*cos(theta1))/(L1*L2*cos(theta2))]])
    omega_d = Jinv @ K @ axis_f
    omega_d = np.squeeze(np.asarray(omega_d))
    command.velocity = omega_d
    group.send_command(command)


def animate_ball(window,canvas,pos,ball_traj):
    canvas.coords(ball_traj,
                pos[0]-animation_ball_radius,
                pos[1]-animation_ball_radius,
                pos[0]+animation_ball_radius,
                pos[1]+animation_ball_radius)
    window.update()

def encoder_draw(window,canvas,arduino,ball_input,offset,draw):
    theta = get_encoder_feedback(arduino, num_encoders=2)

    pos = 5000*np.array([-L1*np.sin(theta[0]) - L2*np.cos(theta[0]+theta[1]), L1*np.cos(theta[0])-L2*np.sin(theta[0]+theta[1])])
    pos[1] = animation_window_height - pos[1]
    pos += offset
    if draw == True:
        canvas.coords(ball_input,
                      pos[0]-encoder_ball_radius,
                      pos[1]-encoder_ball_radius,
                      pos[0]+encoder_ball_radius,
                      pos[1]+encoder_ball_radius)
        window.update()

    print(pos)
    return pos


if __name__ == "__main__":

    animation_window = create_animation_window()
    animation_canvas = create_animation_canvas(animation_window)
    traj = initialize_trajectory("lissajous_005.csv")

    pos = trajectory(0, traj)
    offset = np.array([0, 0])

    ball_traj = animation_canvas.create_oval(pos[0]-animation_ball_radius,
                                             pos[1]-animation_ball_radius,
                                             pos[0]+animation_ball_radius,
                                             pos[1]+animation_ball_radius,
                                             fill="red")

    ball_input = animation_canvas.create_oval(pos[0]-encoder_ball_radius,
                                              pos[1]-encoder_ball_radius,
                                              pos[0]+encoder_ball_radius,
                                              pos[1]+encoder_ball_radius,
                                              fill="white")

    animation_window.update()


    freq = 100 # hz
    group, hebi_feedback, command = initialize_hebi()
    group.feedback_frequency = freq
    joystick = initialize_joystick()
    output = []

    arduino = initialize_encoders()
    group_info = group.request_info()

    print("Get ready...")
    sleep(5)
    pos_draw = encoder_draw(animation_window,animation_canvas,arduino,ball_input,offset,draw=False)
    offset = pos - pos_draw

    if group_info is not None:
        group_info.write_gains("csv/saved_gains.xml")



    #=== variables for 2 dof ===#
    L1 = 0.29
    L2 = 0.22
    #======#

    #=== variables for 3 dof ===#
    # l1 = 0.268
    # l2 = 0.472
    #======#


    i = 0

    t0 = time()
    K = np.matrix([[0.125, 0],
                   [0, 0.125]])

    while True:

       theta, omega, torque, hebi_limit_stop_flag = get_hebi_feedback(group, hebi_feedback)  
       t = time() - t0
       pos = trajectory(t, traj)
       animate_ball(animation_window,animation_canvas,pos,ball_traj)
       pos_draw = encoder_draw(animation_window,animation_canvas,arduino,ball_input,offset,draw=True)
       axis = get_axis(joystick)
       axis[1] = -axis[1]
       theta_e = get_encoder_feedback(arduino, num_encoders=2)
       theta = theta + np.array([-1.58170749, np.pi/2 - 1.48693642])   # offsetting transform
       theta1 = theta[0]
       theta2 = theta[1]
       print(axis)
       axis_f = input_filter(axis, 10, t)

       Jinv = np.matrix([[-cos(theta1 + theta2)/(L1*cos(theta2)), -sin(theta1 + theta2)/(L1*cos(theta2))],
                         [(L2*cos(theta1 + theta2) + L1*sin(theta1))/(L1*L2*cos(theta2)), (L2*sin(theta1 + theta2) - L1*cos(theta1))/(L1*L2*cos(theta2))]])


       omega_d = Jinv @ K @ axis_f
       omega_d = np.squeeze(np.asarray(omega_d))
       command.velocity = omega_d
       # print(omega_d)
       group.send_command(command)

       output += [[t, theta[0], theta[1] , omega_d[0], omega_d[1], omega[0], omega[1], axis[0], axis[1], axis_f[0], axis_f[1]]]

       if i == 0:
           print("ready to operate...")
           i = 1


       if keyboard.is_pressed('esc'):
           save_data(output)
           break


