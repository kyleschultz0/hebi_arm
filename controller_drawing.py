import tkinter
from time import time, sleep
import pandas as pd
import numpy as np
import keyboard
from controller_input import initialize_joystick, get_axis



 
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

def initialize_trajectory(filepath):
    df = pd.read_csv(filepath, names=["t", "x", "y"])
    return(df)

def trajectory(t, df):
    tTraj = df.t
    x = df.x
    y = df.y
    xd = np.interp(t, tTraj, x)
    yd = np.interp(t, tTraj, y)
    pos = np.array([xd, yd])
    return pos
 
# Create and animate ball in an infinite loop
def animate_ball(window,canvas,pos):
    ball = canvas.create_oval(pos[0]-animation_ball_radius,
            pos[1]-animation_ball_radius,
            pos[0]+animation_ball_radius,
            pos[1]+animation_ball_radius,
            fill="red")
    window.update()

def controller_draw(window,canvas,joystick,pos_last,t_draw):
    input = get_axis(joystick)
    delta_t = time() - t_draw
    delta_pos = input*delta_t*300
    pos = pos_last + delta_pos
    t_draw = time()
    ball = canvas.create_oval(pos[0]-encoder_ball_radius,
            pos[1]-encoder_ball_radius,
            pos[0]+encoder_ball_radius,
            pos[1]+encoder_ball_radius,
            fill="white")
    window.update()
    return pos, t_draw

if __name__ == "__main__":
    joystick = initialize_joystick()
    animation_window = create_animation_window()
    animation_canvas = create_animation_canvas(animation_window)
    traj = initialize_trajectory("lissajous_005.csv")
    t0 = time()
    pos_draw = trajectory(0, traj)
    t_draw = t0
    while True:
        t = time() - t0
        pos = trajectory(t, traj)
        animate_ball(animation_window,animation_canvas,pos)
        pos_draw, t_draw = controller_draw(animation_window,animation_canvas,joystick,pos_draw,t_draw)

        if keyboard.is_pressed('esc'):
            print("Stopping: User input stop command")
            break


