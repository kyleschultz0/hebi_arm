import pandas as pd
import os
import glob
import numpy as np

def initialize_trajectory(frequency):
    retval = os.getcwd()
    print("Current working directory", retval)
    os.chdir("trajectories")
    if os.path.exists("combined_trajectories.csv"):
        os.remove("combined_trajectories.csv")
    else:
        print("The file does not exist")
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    print(all_filenames)
    #combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ], sort=False, ignore_index=True)
    length = len(combined_csv)
    times = np.linspace(0, (1/frequency)*length, length, endpoint=False)
    timesdf = pd.DataFrame(times, columns = ['t'])
    print("Times", timesdf)
    print("CSV", combined_csv)
   # combined_csv_times = pd.concat([timesdf, combined_csv], sort=False)
    combined_csv['t'] = timesdf
    print(combined_csv)
    #export to csv
    combined_csv.to_csv( "combined_trajectories.csv", index=False, encoding='utf-8-sig')

    

def trajectory(t, filepath):
    df = pd.read_csv(filepath)
    tTraj = df.t
    theta1 = df.theta1
    theta2 = df.theta2
    theta1 = np.interp(t, tTraj, theta1)
    theta2 = np.interp(t, tTraj, theta2)
    theta = np.array([theta1, theta2])
    print("Trajectory output:", theta)
    return theta

# to test functions:
if __name__ == "__main__":
    initialize_trajectory(50)
    theta = trajectory(1, "combined_trajectories.csv")