import tkinter
import time
import pandas as pd
import encoder_functions


 
# width of the animation window
animation_window_width=1000
# height of the animation window
animation_window_height=1000
# radius of the ball
animation_ball_radius = 10
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
    yd = np.interp(t, tTraj, u)
    pos = np.array([xd, yd])
    return pos
 
# Create and animate ball in an infinite loop
def animate_ball(window,canvas,traj):
    n = len(traj)
    ball = canvas.create_oval(traj.x[0]-animation_ball_radius,
            traj.y[0]-animation_ball_radius,
            traj.x[0]+animation_ball_radius,
            traj.y[0]+animation_ball_radius,
            fill="red")


if __name__ == "__main__":
    animation_window = create_animation_window()
    animation_canvas = create_animation_canvas(animation_window)
    traj = initialize_trajectory("lissajous_005.csv")
    animate_ball(animation_window,animation_canvas,traj)
