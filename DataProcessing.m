clc; clear all; close all;

%% Setup the Import Options and import the data
opts = delimitedTextImportOptions("NumVariables", 11);

% Specify range and delimiter
opts.DataLines = [1, Inf];
opts.Delimiter = ",";

% Specify column names and types
opts.VariableNames = ["t", "h_theta1", "h_theta2", "h_omega1", "h_omega2",...
    "f_torque1", "f_torque2", "c_torque1", "c_torque2", "e_theta1", "e_theta2"];
opts.VariableTypes = ["double", "double", "double", "double", "double",...
    "double", "double", "double", "double", "double", "double"];

% Specify file level properties
opts.ImportErrorRule = "omitrow";
opts.MissingRule = "omitrow";
opts.ExtraColumnsRule = "ignore";
opts.EmptyLineRule = "read";

% Import the data
testdata1 = readtable("csv/circle_5_15", opts);

% Clear temporary variables
clear opts

%% Plot data

% testdata1 = testdata1(1000:end, :);


figure;
plot(testdata1.t, testdata1.h_theta1, 'b-', testdata1.t, testdata1.e_theta1, 'b--',...
    testdata1.t, testdata1.h_theta2, 'r-', testdata1.t, testdata1.e_theta2, 'r--');
% ylim([0 3.5]);
legend("HEBI Angle 1", "Encoder Angle 1", "HEBI Angle 2", "Encoder Angle 2");

