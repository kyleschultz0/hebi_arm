import tkinter
from time import time, sleep
import pandas as pd
import numpy as np
import keyboard
from encoder_functions import initialize_encoders, get_encoder_feedback



 
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


def save_data(output):
    np.savetxt("csv/DrawingTest1.csv", np.array(output), delimiter=",")
    print("Data saved")


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
def animate_ball(window,canvas,pos,ball_traj):
    canvas.coords(ball_traj,
                pos[0]-animation_ball_radius,
                pos[1]-animation_ball_radius,
                pos[0]+animation_ball_radius,
                pos[1]+animation_ball_radius)
    window.update()

def encoder_draw(animation_window,animation_canvas,arduino,ball_input):
    theta = get_encoder_feedback(arduino, num_encoders=2)
    pos = 1000*np.array([L1*np.sin(theta[0]) + L2*np.cos(theta[1]), L1*np.cos(theta[0])-L2*np.sin(theta[1])])
    canvas.coords(ball_input,
                pos[0]-encoder_ball_radius,
                pos[1]-encoder_ball_radius,
                pos[0]+encoder_ball_radius,
                pos[1]+encoder_ball_radius)
    window.update()
    return pos

if __name__ == "__main__":
    output = []
    arduino = initialize_encoders()
    animation_window = create_animation_window()
    animation_canvas = create_animation_canvas(animation_window)
    traj = initialize_trajectory("lissajous_005.csv")
    pos = trajectory(0, traj)

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

    t0 = time()
    while True:
        t = time() - t0
        pos = trajectory(t, traj)
        animate_ball(animation_window,animation_canvas,pos,ball_traj)
        encoder_draw(animation_window,animation_canvas,arduino,ball_input)
        output += [[t,pos[0],pos[1],pos_draw[0],pos_draw[1]]]

        if keyboard.is_pressed('esc'):
            print("Stopping: User input stop command")
            save_data(output)
            break



