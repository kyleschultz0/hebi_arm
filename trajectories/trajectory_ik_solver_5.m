%% uses robotics toolkit ik solver to generate joint angles and save csv

close all; clear all; clc

%% settings

animate = 0;
save = 1;

%% define trajectory
% each timestep will be one control timestep (will take 0.02 sec)

T = 0.01;
center = [0 0.62 0];

D = 0.20;
force_endpoint = 1;
line_time = 4;

save_filename = 'star0.csv';
[points, count] = star(line_time, D, T, center, force_endpoint);
solve_ik(points, count, T, animate, save, save_filename);

function solve_ik(points, count, T, animate, save, save_filename)
    L1 = 0.27;
    L2 = 0.47;

    % create rigid body tree
    robot = rigidBodyTree('DataFormat','column','MaxNumBodies',2);

    body = rigidBody('link1');
    joint = rigidBodyJoint('joint1', 'revolute');
    setFixedTransform(joint,trvec2tform([0 0 0]));
    joint.JointAxis = [0 0 1];
    body.Joint = joint;
    addBody(robot, body, 'base');

    body = rigidBody('link2');
    joint = rigidBodyJoint('joint2','revolute');
    setFixedTransform(joint, trvec2tform([L1,0,0]));
    joint.JointAxis = [0 0 1];
    body.Joint = joint;
    addBody(robot, body, 'link1');

    body = rigidBody('tool');
    joint = rigidBodyJoint('fix1','fixed');
    setFixedTransform(joint, trvec2tform([L2, 0, 0]));
    body.Joint = joint;
    addBody(robot, body, 'link2');

    % showdetails(robot)

    % for configuration solutions
    q0 = [pi/4, pi/2]';
    ndof = length(q0);
    qs = zeros(count, 2*ndof+1);

    % create solver
    ik = inverseKinematics('RigidBodyTree', robot);
    weights = [0, 0, 0, 1, 1, 0];
    endEffector = 'tool';

    % loop through trajectory
    qInitial = q0; % Use home configuration as the initial guess
    for i = 1:count
        % Solve for the configuration satisfying the desired end effector
        % position
        point = points(i,:);
        qSol = ik(endEffector,trvec2tform(point),weights,qInitial);
        % Store the configuration
        qs(i,4:end) = qSol;
        % Start from prior solution
        qInitial = qSol;
    end

    if save        
        t = 0:T:T*(count-1);
        qs(2:end, 2:3) = diff(qs(:,4:end))./T;
        qs(:, 1) = t.';
        writematrix(qs,save_filename)
    end

    if animate
        figure
        show(robot,qs(1,4:end)');
        view(2)
        ax = gca;
        ax.Projection = 'orthographic';
        hold on

        plot(points(:,1),points(:,2),'k', 'Linewidth',1.5);
        framesPerSecond = 200;
        r = rateControl(framesPerSecond);
        for i = 1:count
            show(robot,qs(i,4:end)','PreservePlot',false);
            axis([-0.6, 0.6, 0, 1.25])
            drawnow
            waitfor(r);
        end
        hold off
    end
end

function [points, count] = MJLT(p1, p2, tf, T, force_endpoint)
    % point 1, point 2, total time, timestep
    % MJLT: minimum jerk line trajectory
    % for 2D straight line trajectory
    
    % create time vector:
    t = [0];
    while t(end) < tf
        t = [t; t(end)+T];
    end
    count = length(t);
    
    % create minimum jerk trajectory along line:
    rf = sqrt((p2(1)-p1(1))^2 + (p2(2)-p1(2))^2);
    r = rf*(6.*(t./tf).^5 - 15.*(t./tf).^4 + 10.*(t./tf).^3);
        
    % convert trajectory to x-y coordinates
    theta = atan2(p2(2)-p1(2), p2(1)-p1(1));
    x = r.*cos(theta) + p1(1);
    y = r.*sin(theta) + p1(2);
    if force_endpoint
        x(end) = p2(1);
        y(end) = p2(2);
    end
    z = zeros([count,1]);
    points = [x,y,z];
end

function [points, count] = star(line_time, D, T, center, force_endpoint)
% D = diameter of circumscribed circle
% T = sampling rate
    
    % define verticies
    v1 = center + [0, D/2, 0];
    v2 = center + [D/2*sind(72), D/2*cosd(72), 0];
    v3 = center + [D/2*sind(144), D/2*cosd(144), 0];
    v4 = center + [D/2*sind(216), D/2*cosd(216), 0];
    v5 = center + [D/2*sind(288), D/2*cosd(288), 0];
    
    % generate trajectory points   
    [points41, count41] = MJLT(v4, v1, line_time, T, force_endpoint);
    [points13, count13] = MJLT(v1, v3, line_time, T, force_endpoint);
    [points35, count35] = MJLT(v3, v5, line_time, T, force_endpoint);
    [points52, count52] = MJLT(v5, v2, line_time, T, force_endpoint);
    [points24, count24] = MJLT(v2, v4, line_time, T, force_endpoint);
    
    points = [points41; points13; points35; points52; points24];
    count = count41 + count13 + count35 + count52 + count24;
end
