import tkinter
from time import time, sleep
import pandas as pd
import numpy as np
from encoder_functions import initialize_encoders, get_encoder_feedback
import keyboard
from controller_input import initialize_joystick, get_axis
from controller_operation import controller_operation
from hebi_functions import initialize_hebi, get_hebi_feedback, send_hebi_position_command, send_hebi_effort_command


 
# width of the animation window
animation_window_width=1000
# height of the animation window
animation_window_height=1000
# radius of the ball
animation_ball_radius = 10
# radius of the encoder ball
encoder_ball_radius = 5
# delay between successive frames in seconds
animation_refresh_seconds = 0.01

#=== Variables for 2 DOF ===#
L1 = 0.29
L2 = 0.22
#======#

#=== Variables for 3 DOF ===#
# L1 = 0.268
# L2 = 0.472
#======#

 
# The main window of the animation
def create_animation_window():
  window = tkinter.Tk()
  window.title("Tkinter Animation Demo")
  # Uses python 3.6+ string interpolation
  window.geometry(f'{animation_window_width}x{animation_window_height}')
  return window
 
# Create a canvas for animation and add it to main window
def create_animation_canvas(window):
  canvas = tkinter.Canvas(window)
  canvas.configure(bg="black")
  canvas.pack(fill="both", expand=True)
  return canvas


def encoder_draw(window,canvas,arduino, L1, L2):
    theta = get_encoder_feedback(arduino, num_encoders=2)
    pos = 1000*np.array([L1*np.sin(theta[0]) + L2*np.cos(theta[1]), L1*np.cos(theta[0])-L2*np.sin(theta[1])])
    pos = pos + np.array([400, 400])
    print(pos)
    ball = canvas.create_oval(pos[0]-encoder_ball_radius,
            pos[1]-encoder_ball_radius,
            pos[0]+encoder_ball_radius,
            pos[1]+encoder_ball_radius,
            fill="white")
    window.update()

if __name__ == "__main__":
    arduino = initialize_encoders()
    animation_window = create_animation_window()
    animation_canvas = create_animation_canvas(animation_window)
    t0 = time()
    while True:
        encoder_draw(animation_window,animation_canvas,arduino, L1, L2)

        if keyboard.is_pressed('esc'):
            print("Stopping: User input stop command")
            break

