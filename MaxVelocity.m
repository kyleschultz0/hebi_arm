% Kyle Schultz
% Computing max velocity of trajectory

clc; clear all; close all;

syms C f t d ab

ab = 0.5

% Window size, frequency, time, offset, y scalar


x = C*sin(2*pi*f*t+d);
y = C*cos(2*pi*f*ab*t);

d_sq = x^2 + y^2;

v_sq = diff(d_sq, t)

a_sq = diff(v_sq, t)

solve(a_sq == 0, t)