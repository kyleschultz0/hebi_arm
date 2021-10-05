clc; clear all; close all;

dataHebi1 = importfileEncoder("controller5.csv");
figure;
plot(dataHebi1.pos1, dataHebi1.pos2, dataHebi1.posDraw1, dataHebi1.posDraw2)
legend("Desired", "Actual")
title("Output Without Cables")

dataEncoder1 = importfileHebi("controller12.csv");
figure;
plot(dataEncoder1.pos1, dataEncoder1.pos2, dataEncoder1.posDraw1, dataEncoder1.posDraw2)
legend("Desired", "Actual")
title("Output With Cables")

%% Import functions

function data = importfileEncoder(filename, dataLines)
%% Input handling

% If dataLines is not specified, define defaults
if nargin < 2
    dataLines = [1, Inf];
end

%% Set up the Import Options and import the data
opts = delimitedTextImportOptions("NumVariables", 14);

% Specify range and delimiter
opts.DataLines = dataLines;
opts.Delimiter = ",";

% Specify column names and types
opts.VariableNames = ["t", "thetaH1", "thetaH2", "thetaE1", "thetaE2", "omegaD1", "omegaD2", "omega1", "omega2", "useless", "pos1", "pos2", "posDraw1", "posDraw2"];
opts.VariableTypes = ["double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double"];

% Specify file level properties
opts.ExtraColumnsRule = "ignore";
opts.EmptyLineRule = "read";

% Import the data
data = readtable(filename, opts);

end

function data = importfileHebi(filename, dataLines)
%% Input handling

% If dataLines is not specified, define defaults
if nargin < 2
    dataLines = [1, Inf];
end

%% Set up the Import Options and import the data
opts = delimitedTextImportOptions("NumVariables", 12);

% Specify range and delimiter
opts.DataLines = dataLines;
opts.Delimiter = ",";

% Specify column names and types
opts.VariableNames = ["t", "theta1", "theta2", "omegad1", "omegad2", "omega1", "omega2", "useless", "pos1", "pos2", "posDraw1", "posDraw2"];
opts.VariableTypes = ["double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double"];

% Specify file level properties
opts.ExtraColumnsRule = "ignore";
opts.EmptyLineRule = "read";

% Import the data
data = readtable(filename, opts);

end