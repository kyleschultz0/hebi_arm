clc; clear all; close all;

dataController1 = importfileController("R2Drawing1.csv");
figure;
plot(dataController1.pos1, dataController1.pos2, dataController1.posDraw1, dataController1.posDraw2)
legend("Desired", "Actual")
title("Output With Contoller")

dataHebi1 = importfileHebi("R2Drawing7.csv");
figure;
plot(dataHebi1.pos1, dataHebi1.pos2, dataHebi1.posDraw1, dataHebi1.posDraw2)
legend("Desired", "Actual")
title("Output Without Cables")

dataEncoder1 = importfileEncoder("R2Drawing12.csv");
figure;
plot(dataEncoder1.pos1, dataEncoder1.pos2, dataEncoder1.posDraw1, dataEncoder1.posDraw2)
legend("Desired", "Actual")
title("Output With Cables")

figure;
plot(dataController1.pos1, dataController1.pos2, dataController1.posDraw1, dataController1.posDraw2, ...
    dataHebi1.posDraw1, dataHebi1.posDraw2,...
    dataEncoder1.posDraw1, dataEncoder1.posDraw2)
title("Operator Output Tracking")
legend("Desired", "Controller Only", "HEBIs", "Cables")


%%

dataController1 = importfileController("R2Drawing1.csv");
dataController2 = importfileController("R2Drawing2.csv");
dataController3 = importfileController("R2Drawing4.csv");
dataController4 = importfileController("R2Drawing5.csv");
dataController5 = importfileController("R2Drawing6.csv");

RMSEC1 = sum((sqrt((dataController1.posDraw1-dataController1.pos1).^2+(dataController1.posDraw2-dataController1.pos2).^2))/height(dataController1));
RMSEC2 = sum((sqrt((dataController2.posDraw1-dataController2.pos1).^2+(dataController2.posDraw2-dataController2.pos2).^2))/height(dataController2));
RMSEC3 = sum((sqrt((dataController3.posDraw1-dataController3.pos1).^2+(dataController3.posDraw2-dataController3.pos2).^2))/height(dataController3));
RMSEC4 = sum((sqrt((dataController4.posDraw1-dataController4.pos1).^2+(dataController4.posDraw2-dataController4.pos2).^2))/height(dataController4));
RMSEC5 = sum((sqrt((dataController5.posDraw1-dataController5.pos1).^2+(dataController5.posDraw2-dataController5.pos2).^2))/height(dataController5));

figure;
title("Error with Different Inputs")
plot([0.05/4, 0.05/2, 0.05/1, 0.05*2, 0.05*4], [RMSEC1, RMSEC2, RMSEC3, RMSEC4, RMSEC5], 'r*')
xlabel("Frequency (Hz)")
ylabel("RMSE")
hold on
%% HEBI

dataController1 = importfileHebi("R2Drawing7.csv");
dataController2 = importfileHebi("R2Drawing8.csv");
dataController3 = importfileHebi("R2Drawing9.csv");
dataController4 = importfileHebi("R2Drawing10.csv");
dataController5 = importfileHebi("R2Drawing11.csv");

RMSEH1 = sum((sqrt((dataController1.posDraw1-dataController1.pos1).^2+(dataController1.posDraw2-dataController1.pos2).^2))/height(dataController1));
RMSEH2 = sum((sqrt((dataController2.posDraw1-dataController2.pos1).^2+(dataController2.posDraw2-dataController2.pos2).^2))/height(dataController2));
RMSEH3 = sum((sqrt((dataController3.posDraw1-dataController3.pos1).^2+(dataController3.posDraw2-dataController3.pos2).^2))/height(dataController3));
RMSEH4 = sum((sqrt((dataController4.posDraw1-dataController4.pos1).^2+(dataController4.posDraw2-dataController4.pos2).^2))/height(dataController4));
RMSEH5 = sum((sqrt((dataController5.posDraw1-dataController5.pos1).^2+(dataController5.posDraw2-dataController5.pos2).^2))/height(dataController5));


title("Error with HEBI")
plot([0.05/4, 0.05/2, 0.05/1, 0.05*2, 0.05*4], [RMSEH1, RMSEH2, RMSEH3, RMSEC4, RMSEH5], 'g*')
xlabel("Frequency (Hz)")
ylabel("RMSE")
%%

%% Encoder

dataController1 = importfileEncoder("R2Drawing12.csv");
dataController2 = importfileEncoder("R2Drawing13.csv");
dataController3 = importfileEncoder("R2Drawing14.csv");
dataController4 = importfileEncoder("R2Drawing15.csv");

RMSEE1 = sum((sqrt((dataController1.posDraw1-dataController1.pos1).^2+(dataController1.posDraw2-dataController1.pos2).^2))/height(dataController1));
RMSEE2 = sum((sqrt((dataController2.posDraw1-dataController2.pos1).^2+(dataController2.posDraw2-dataController2.pos2).^2))/height(dataController2));
RMSEE3 = sum((sqrt((dataController3.posDraw1-dataController3.pos1).^2+(dataController3.posDraw2-dataController3.pos2).^2))/height(dataController3));
RMSEE4 = sum((sqrt((dataController4.posDraw1-dataController4.pos1).^2+(dataController4.posDraw2-dataController4.pos2).^2))/height(dataController4));


title("Error with HEBI")
plot([0.05/4, 0.05/2, 0.05/1, 0.05*2], [RMSEE1, RMSEE2, RMSEE3, RMSEE4], 'b*')
xlabel("Frequency (Hz)")
ylabel("RMSE")
hold off
legend("Controller", "HEBI", "Encoder")
xlim([0 0.25])
%% Import functions

function data = importfileController(filename, dataLines)

%% Input handling

% If dataLines is not specified, define defaults
if nargin < 2
    dataLines = [1, Inf];
end

%% Set up the Import Options and import the data
opts = delimitedTextImportOptions("NumVariables", 5);

% Specify range and delimiter
opts.DataLines = dataLines;
opts.Delimiter = ",";

% Specify column names and types
opts.VariableNames = ["t", "pos1", "pos2", "posDraw1", "posDraw2"];
opts.VariableTypes = ["double", "double", "double", "double", "double"];

% Specify file level properties
opts.ExtraColumnsRule = "ignore";
opts.EmptyLineRule = "read";

% Import the data
data = readtable(filename, opts);

end

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