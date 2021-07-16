import pandas as pd
import os
import glob
import numpy as np

#def initialize_trajectory(frequency):
#    retval = os.getcwd()
#    print("Current working directory", retval)
#    os.chdir("trajectories")
#    if os.path.exists("combined_trajectories.csv"):
#        os.remove("combined_trajectories.csv")
#    else:
#        print("The file does not exist")
#    extension = 'csv'
#    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
#    print(all_filenames)
#    #combine all files in the list
#    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ], sort=False, ignore_index=True)
#    length = len(combined_csv)
#    times = np.linspace(0, (1/frequency)*length, length, endpoint=False)
#    timesdf = pd.DataFrame(times, columns = ['t'])
#    print("Times", timesdf)
#    print("CSV", combined_csv)
#   # combined_csv_times = pd.concat([timesdf, combined_csv], sort=False)
#    combined_csv['t'] = timesdf
#    print(combined_csv)
#    #export to csv
#    combined_csv.to_csv( "combined_trajectories.csv", index=False, encoding='utf-8-sig')
#    os.chdir('..')

def initialize_trajectory(filepath):
    df = pd.read_csv(filepath)
    return(df)

    

def trajectoryold(t, filepath):
    df = pd.read_csv(filepath)
    tTraj = df.t
    theta1 = df.theta1
    theta2 = df.theta2
    theta1 = np.interp(t, tTraj, theta1)
    theta2 = np.interp(t, tTraj, theta2)
    theta = np.array([theta1, theta2])
    print("Trajectory output:", theta)
    return theta

def trajectory(t, df):
    #df = pd.read_csv(filepath,
    #                 names=["t", "omega1", "omega2", "theta1", "theta2"])
    tTraj = df.t
    theta1 = df.theta1
    theta2 = df.theta2
    theta1 = np.interp(t, tTraj, theta1)
    theta2 = np.interp(t, tTraj, theta2)
    theta = np.array([theta1, theta2])
    omega1 = df.omega1
    omega2 = df.omega2
    omega1 = np.interp(t, tTraj, omega1)
    omega2 = np.interp(t, tTraj, omega2)
    omega = np.array([omega1, omega2])
    return t, theta, omega

# to test functions:
if __name__ == "__main__":
    t, theta_d, omega_d = trajectory(1, "trajectories/cstar_20_20.csv")
    print(t)
    print(theta_d)
    print(omega_d)
   