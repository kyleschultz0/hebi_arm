%% Script to generate sinusoidal csv file for arm trajectories

clc; clear all; close all;

f = 0.5;    % frequency (Hz)
A = 3;
outputFile = "trajectories_3sin05.csv";

t = linspace(0, 25, 2001)';
x2 = 0.*t;
x1 = A*sin(2*pi*f*t);
traj = [t x1 x2];

figure;
plot(t, x1, t, x2);
legend("Joint 1", "Joint 2");
title("Joint Trajectories");


writematrix(traj, outputFile)