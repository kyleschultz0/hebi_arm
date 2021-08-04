clc; clear all; close all;

%% Setup the Import Options and import the data
opts = delimitedTextImportOptions("NumVariables", 9);

% Specify range and delimiter
opts.DataLines = [1, Inf];
opts.Delimiter = ",";


%% For velocity assistance ------------------------------------------------

% opts.VariableNames = ["t", "h_theta1", "h_theta2", "h_omega1", "h_omega2",...
%     "f_torque1", "f_torque2", "c_torque1", "c_torque2", "e_theta1", "e_theta2"];

% opts.VariableTypes = ["double", "double", "double", "double", "double",...
%     "double", "double", "double", "double", "double", "double"];
% -------------------------------------------------------------------------

%% For force assistance ---------------------------------------------------
opts.VariableNames = ["t", "h_theta1", "h_theta2", "torqued1", "torqued2",...
    "torque1", "torque2", "f_adjust1", "f_adjust2"];

opts.VariableTypes = ["double", "double", "double", "double", "double",...
    "double", "double", "double", "double"];
% -------------------------------------------------------------------------




% Specify file level properties
opts.ImportErrorRule = "omitrow";
opts.MissingRule = "omitrow";
opts.ExtraColumnsRule = "ignore";
opts.EmptyLineRule = "read";

% Import the data
testdata1 = readtable("csv/assistance_force2", opts);
testdata1.t = testdata1.t - testdata1.t(1);

% Clear temporary variables
clear opts

%% Plot data

% testdata1 = testdata1(1000:end, :);


figure;
plot(testdata1.t, testdata1.h_theta1, testdata1.t, testdata1.h_theta2, ...
     testdata1.t, testdata1.torqued1, testdata1.t, testdata1.torqued2, ...
     testdata1.t, testdata1.torque1, testdata1.t, testdata1.torque2,...
     testdata1.t, testdata1.f_adjust1, testdata1.t, testdata1.f_adjust2);
% ylim([0 3.5]);
legend("HEBI Angle 1", "HEBI Angle 2", "Desired Torque 1", "Desired Torque 2", ...
    "Feedback Torque 1", "Feedback Torque 2", "Adjusted Force Reading -x", "Adjusted Force Reading -y");
