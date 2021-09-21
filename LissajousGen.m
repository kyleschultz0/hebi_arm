% Kyle Schultz
% Generate Lissajous curve for trajectory

clc; clear all; close all

time_plot = false;   % Plot over time
t_step = 0.01;
f = 0.05;
a = 2*pi*f;
t = 0:t_step:1/f;
a_per_b = 0.5;
b = a/a_per_b;
window_size = 400; % square window
d = pi/4;

x = window_size + 50 + round(window_size*sin(a*t+d));
y = window_size + 50 + round(window_size*cos(b*t));

figure;
hold on
xlim([-1000, 1000]); ylim([-1000, 1000])
if time_plot == true
    for i = 1:numel(x)
        plot(x(1:i), y(1:i))
        pause(1/10000)
    end
else
    plot(x, y)
end

curve = [t' x' y'];
outputFile = "lissajous_" + erase(string(f), ".") + ".csv";
writematrix(curve, outputFile)
