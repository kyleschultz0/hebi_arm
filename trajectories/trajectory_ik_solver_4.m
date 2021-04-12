%% uses robotics toolkit ik solver to generate joint angles and save csv

close all; clear all; clc

%% settings

animate = 1;
save = 1;

%%
% speed = 5;
% shape = 'ccircle';
% [points, count] = circle(speed, D, T, center);
% solve_ik(points, count, speed, D, T, center, shape, animate, save)

%% define trajectory
% each timestep will be one control timestep (will take 0.005 sec)

T = 0.005;
center = [0 0.75 0];

% D = [0.05, 0.10, 0.15, 0.2, 0.25];
% speed = [0.07, 0.11, 0.15, 0.19, 0.23];

D = 0.2;
speed = 0.2;

for i = 1:length(D)
    for j = 1:length(speed)
        shape = 'cstar';
        [points, count] = star(speed(j), D(i), T, center);
        solve_ik(points, count, speed(j), D(i), T, center, shape, animate, save)
    end
end


% % 5
% for i = 1:length(D)
%     for j = 1:length(speed)
%         shape = 'c5';
%         [points, count] = five(speed(j), D(i), T, center);
%         solve_ik(points, count, speed(j), D(i), T, center, shape, animate, save)
%     end
% end
% 
% % 4
% for i = 1:length(D)
%     for j = 1:length(speed)
%         shape = 'c4';
%         [points, count] = four(speed(j), D(i), T, center);
%         solve_ik(points, count, speed(j), D(i), T, center, shape, animate, save)
%     end
% end
% 
% % 8
% for i = 1:length(D)
%     for j = 1:length(speed)
%         shape = 'c8';
%         [points, count] = eight(speed(j), D(i), T, center);
%         solve_ik(points, count, speed(j), D(i), T, center, shape, animate, save)
%     end
% end
% 
% % 1
% for i = 1:length(D)
%     for j = 1:length(speed)
%         shape = 'c1';
%         [points, count] = one(speed(j), D(i), T, center);
%         solve_ik(points, count, speed(j), D(i), T, center, shape, animate, save)
%     end
% end
% 
% % 7
% for i = 1:length(D)
%     for j = 1:length(speed)
%         shape = 'c7';
%         [points, count] = seven(speed(j), D(i), T, center);
%         solve_ik(points, count, speed(j), D(i), T, center, shape, animate, save)
%     end
% end
% 
% % W
% for i = 1:length(D)
%     for j = 1:length(speed)
%         shape = 'cW';
%         [points, count] = W(speed(j), D(i), T, center);
%         solve_ik(points, count, speed(j), D(i), T, center, shape, animate, save)
%     end
% end
% 
% % V
% for i = 1:length(D)
%     for j = 1:length(speed)
%         shape = 'cV';
%         [points, count] = V(speed(j), D(i), T, center);
%         solve_ik(points, count, speed(j), D(i), T, center, shape, animate, save)
%     end
% end
% 
% % N
% for i = 1:length(D)
%     for j = 1:length(speed)
%         shape = 'cN';
%         [points, count] = N(speed(j), D(i), T, center);
%         solve_ik(points, count, speed(j), D(i), T, center, shape, animate, save)
%     end
% end
% 
% % L
% for i = 1:length(D)
%     for j = 1:length(speed)
%         shape = 'cL';
%         [points, count] = L(speed(j), D(i), T, center);
%         solve_ik(points, count, speed(j), D(i), T, center, shape, animate, save)
%     end
% end
% 
% % Z
% for i = 1:length(D)
%     for j = 1:length(speed)
%         shape = 'cZ';
%         [points, count] = Z(speed(j), D(i), T, center);
%         solve_ik(points, count, speed(j), D(i), T, center, shape, animate, save)
%     end
% end
% 
% % circle
% for i = 1:length(D)
%     for j = 1:length(speed)
% shape = 'ccircle';
% [points, count] = circle(speed(j), D(i), T, center);
% solve_ik(points, count, speed(j), D(i), T, center, shape, animate, save)
%     end
% end
% 
% % square
% for i = 1:length(D)
%     for j = 1:length(speed)
% shape = 'csquare';
% [points, count] = square(speed(j), D(i), T, center);
% solve_ik(points, count, speed(j), D(i), T, center, shape, animate, save)
%     end
% end
% 
% % pentagon
% for i = 1:length(D)
%     for j = 1:length(speed)
% shape = 'cpentagon';
% [points, count] = pentagon(speed(j), D(i), T, center);
% solve_ik(points, count, speed(j), D(i), T, center, shape, animate, save)
%     end
% end
% 
% % hexagon
% for i = 1:length(D)
%     for j = 1:length(speed)
% shape = 'chexagon';
% [points, count] = hexagon(speed(j), D(i), T, center);
% solve_ik(points, count, speed(j), D(i), T, center, shape, animate, save)
%     end
% end
% 
% % star
% for i = 1:length(D)
%     for j = 1:length(speed)
% shape = 'cstar';
% [points, count] = star(speed(j), D(i), T, center);
% solve_ik(points, count, speed(j), D(i), T, center, shape, animate, save)
%     end
% end
% 
% % circle
% for i = 1:length(D)
%     for j = 1:length(speed)
% shape = 'rcircle';
% [points, count] = circle(speed(j), D(i), T, center);
% points = flip(points);
% solve_ik(points, count, speed(j), D(i), T, center, shape, animate, save)
%     end
% end
% 
% % square
% for i = 1:length(D)
%     for j = 1:length(speed)
% shape = 'rsquare';
% [points, count] = square(speed(j), D(i), T, center);
% points = flip(points);
% solve_ik(points, count, speed(j), D(i), T, center, shape, animate, save)
%     end
% end
% 
% % pentagon
% for i = 1:length(D)
%     for j = 1:length(speed)
% shape = 'rpentagon';
% [points, count] = pentagon(speed(j), D(i), T, center);
% points = flip(points);
% solve_ik(points, count, speed(j), D(i), T, center, shape, animate, save)
%     end
% end
% 
% % hexagon
% for i = 1:length(D)
%     for j = 1:length(speed)
% shape = 'rhexagon';
% [points, count] = hexagon(speed(j), D(i), T, center);
% points = flip(points);
% solve_ik(points, count, speed(j), D(i), T, center, shape, animate, save)
%     end
% end
% 
% % star
% for i = 1:length(D)
%     for j = 1:length(speed)
% shape = 'rstar';
% [points, count] = star(speed(j), D(i), T, center);
% points = flip(points);
% solve_ik(points, count, speed(j), D(i), T, center, shape, animate, save)
%     end
% end


function solve_ik(points, count, speed, D, T, center, shape, animate, save)

    filename_speed = speed*100;
    filename_D = D*100;

    save_filename = strcat(shape, '_'); % format: c{shape}_{speed*100}_{size*100}
    save_filename = strcat(save_filename, num2str(filename_speed)); % format {shape}_{speed*100}_{size*100}
    save_filename = strcat(save_filename, '_');
    save_filename = strcat(save_filename, num2str(filename_D));
    save_filename = strcat(save_filename, '.csv');
    
    L1 = 0.28;
    L2 = 0.6;

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
        
        [circumscribed,~] = circle(0.5, D, T, center);
        plot(circumscribed(:,1),circumscribed(:,2),'--k');
        plot(points(:,1),points(:,2),'k', 'Linewidth',1.5);
        framesPerSecond = 200;
        r = rateControl(framesPerSecond);
        for i = 1:count
            show(robot,qs(i,4:end)','PreservePlot',false);
            drawnow
            waitfor(r);
        end
        hold off
    end
end

function [points, count] = circle(speed, D, T, center)
% D = diameter
% T = sampling rate
    
    % length of trajectory
    circumference = pi*D;
    
    % define number of points
    time = circumference/speed;
    count = round(time/T);

    % generate trajectory points
    t = linspace(0,1,count)';
    theta = t*(2*pi/t(end));
    points = center + D/2*[cos(theta) sin(theta) zeros(size(theta))];
end

function [points, count] = square(speed, D, T, center)
% D = diameter of circumscribed circle
% T = sampling rate
    
    % length of side
    side_length = D/sqrt(2);
    
    % define number of points per side
    time = side_length/speed;
    side_count = round(time/T);

    % define verticies
    v1 = center + [side_length/2, -side_length/2, 0];
    v2 = center + [side_length/2, side_length/2, 0];
    v3 = center + [-side_length/2, side_length/2, 0];
    v4 = center + [-side_length/2, -side_length/2, 0];
    
    % generate trajectory points
    points = [linspace(v1(1), v2(1), side_count)', linspace(v1(2), v2(2), side_count)', zeros(side_count,1)];
    points = [points; linspace(v2(1), v3(1), side_count)', linspace(v2(2), v3(2), side_count)', zeros(side_count,1)];
    points = [points; linspace(v3(1), v4(1), side_count)', linspace(v3(2), v4(2), side_count)', zeros(side_count,1)];
    points = [points; linspace(v4(1), v1(1), side_count)', linspace(v4(2), v1(2), side_count)', zeros(side_count,1)];
    count = 4*side_count;
end

function [points, count] = hexagon(speed, D, T, center)
% D = diameter of circumscribed circle
% T = sampling rate
    
    % length of side
    side_length = D*cos(pi/3);
    
    % define number of points per side
    time = side_length/speed;
    side_count = round(time/T);
    
    % define verticies
    v1 = center + [D/2, 0, 0];
    v2 = center + [D/4, D*sqrt(3)/4, 0];
    v3 = center + [-D/4, D*sqrt(3)/4, 0];
    v4 = center + [-D/2, 0, 0];
    v5 = center + [-D/4, -D*sqrt(3)/4, 0];
    v6 = center + [D/4, -D*sqrt(3)/4, 0];
    
    % generate trajectory points
    points = [linspace(v1(1), v2(1), side_count)', linspace(v1(2), v2(2), side_count)', zeros(side_count,1)];
    points = [points; linspace(v2(1), v3(1), side_count)', linspace(v2(2), v3(2), side_count)', zeros(side_count,1)];
    points = [points; linspace(v3(1), v4(1), side_count)', linspace(v3(2), v4(2), side_count)', zeros(side_count,1)];
    points = [points; linspace(v4(1), v5(1), side_count)', linspace(v4(2), v5(2), side_count)', zeros(side_count,1)];
    points = [points; linspace(v5(1), v6(1), side_count)', linspace(v5(2), v6(2), side_count)', zeros(side_count,1)];
    points = [points; linspace(v6(1), v1(1), side_count)', linspace(v6(2), v1(2), side_count)', zeros(side_count,1)];
    count = 6*side_count;
end

function [points, count] = pentagon(speed, D, T, center)
% D = diameter of circumscribed circle
% T = sampling rate
    
    % length of side
    side_length = D;
    
    % define number of points per side
    time = side_length/speed;
    side_count = round(time/T);
    
    % define verticies
    v1 = center + [0, D/2, 0];
    v2 = center + [D/2*sind(72), D/2*cosd(72), 0];
    v3 = center + [D/2*sind(144), D/2*cosd(144), 0];
    v4 = center + [D/2*sind(216), D/2*cosd(216), 0];
    v5 = center + [D/2*sind(288), D/2*cosd(288), 0];
    
    % generate trajectory points
    points = [linspace(v1(1), v2(1), side_count)', linspace(v1(2), v2(2), side_count)', zeros(side_count,1)];
    points = [points; linspace(v2(1), v3(1), side_count)', linspace(v2(2), v3(2), side_count)', zeros(side_count,1)];
    points = [points; linspace(v3(1), v4(1), side_count)', linspace(v3(2), v4(2), side_count)', zeros(side_count,1)];
    points = [points; linspace(v4(1), v5(1), side_count)', linspace(v4(2), v5(2), side_count)', zeros(side_count,1)];
    points = [points; linspace(v5(1), v1(1), side_count)', linspace(v5(2), v1(2), side_count)', zeros(side_count,1)];
    count = 5*side_count;
end

function [points, count] = star(speed, D, T, center)
% D = diameter of circumscribed circle
% T = sampling rate
    
    % length of side
    side_length = D;
    
    % define number of points per side
    time = side_length/speed;
    side_count = round(time/T);
    
    % define verticies
    v1 = center + [0, D/2, 0];
    v2 = center + [D/2*sind(72), D/2*cosd(72), 0];
    v3 = center + [D/2*sind(144), D/2*cosd(144), 0];
    v4 = center + [D/2*sind(216), D/2*cosd(216), 0];
    v5 = center + [D/2*sind(288), D/2*cosd(288), 0];
    
    % generate trajectory points
    points = [linspace(v4(1), v1(1), side_count)', linspace(v4(2), v1(2), side_count)', zeros(side_count,1)];
    points = [points; linspace(v1(1), v3(1), side_count)', linspace(v1(2), v3(2), side_count)', zeros(side_count,1)];
    points = [points; linspace(v3(1), v5(1), side_count)', linspace(v3(2), v5(2), side_count)', zeros(side_count,1)];
    points = [points; linspace(v5(1), v2(1), side_count)', linspace(v5(2), v2(2), side_count)', zeros(side_count,1)];
    points = [points; linspace(v2(1), v4(1), side_count)', linspace(v2(2), v4(2), side_count)', zeros(side_count,1)];
    count = 5*side_count;
end

function [points, count] = Z(speed, D, T, center)
    % define verticies
    v1 = center + [D/2*cosd(120), D/2*sind(120), 0];
    v2 = center + [D/2*cosd(60), D/2*sind(60), 0];
    v3 = center + [D/2*cosd(240), D/2*sind(240), 0];
    v4 = center + [D/2*cosd(300), D/2*sind(300), 0];
    
    % calculate num_points
    count1 = round(sqrt((v1(1)-v2(1))^2 + (v1(2)-v2(2))^2)/speed/T);
    count2 = round(sqrt((v2(1)-v3(1))^2 + (v2(2)-v3(2))^2)/speed/T);
    count3 = round(sqrt((v3(1)-v4(1))^2 + (v3(2)-v4(2))^2)/speed/T);
    count = count1+count2+count3;
    
    % generate trajectory points
    points = [linspace(v1(1), v2(1), count1)', linspace(v1(2), v2(2), count1)', zeros(count1,1)];
    points = [points; linspace(v2(1), v3(1), count2)', linspace(v2(2), v3(2), count2)', zeros(count2,1)];
    points = [points; linspace(v3(1), v4(1), count3)', linspace(v3(2), v4(2), count3)', zeros(count3,1)];    
end

function [points, count] = L(speed, D, T, center)
    % define verticies
    v1 = center + [D/2*cosd(120), D/2*sind(120), 0];
    v2 = center + [D/2*cosd(240), D/2*sind(240), 0];
    v3 = center + [D/2*cosd(300), D/2*sind(300), 0];
    
    % calculate num_points
    count1 = round(sqrt((v1(1)-v2(1))^2 + (v1(2)-v2(2))^2)/speed/T);
    count2 = round(sqrt((v2(1)-v3(1))^2 + (v2(2)-v3(2))^2)/speed/T);
    count = count1+count2;
    
    % generate trajectory points
    points = [linspace(v1(1), v2(1), count1)', linspace(v1(2), v2(2), count1)', zeros(count1,1)];
    points = [points; linspace(v2(1), v3(1), count2)', linspace(v2(2), v3(2), count2)', zeros(count2,1)];
end

function [points, count] = N(speed, D, T, center)
    % define verticies
    v1 = center + [D/2*cosd(240), D/2*sind(240), 0];
    v2 = center + [D/2*cosd(120), D/2*sind(120), 0];
    v3 = center + [D/2*cosd(300), D/2*sind(300), 0];
    v4 = center + [D/2*cosd(60), D/2*sind(60), 0];
    
    % calculate num_points
    count1 = round(sqrt((v1(1)-v2(1))^2 + (v1(2)-v2(2))^2)/speed/T);
    count2 = round(sqrt((v2(1)-v3(1))^2 + (v2(2)-v3(2))^2)/speed/T);
    count3 = round(sqrt((v3(1)-v4(1))^2 + (v3(2)-v4(2))^2)/speed/T);
    count = count1+count2+count3;
    
    % generate trajectory points
    points = [linspace(v1(1), v2(1), count1)', linspace(v1(2), v2(2), count1)', zeros(count1,1)];
    points = [points; linspace(v2(1), v3(1), count2)', linspace(v2(2), v3(2), count2)', zeros(count2,1)];
    points = [points; linspace(v3(1), v4(1), count3)', linspace(v3(2), v4(2), count3)', zeros(count3,1)];   
end

function [points, count] = V(speed, D, T, center)
    % define verticies
    v1 = center + [D/2*cosd(135), D/2*sind(135), 0];
    v2 = center + [D/2*cosd(270), D/2*sind(270), 0];
    v3 = center + [D/2*cosd(45), D/2*sind(45), 0];
    
    % calculate num_points
    count1 = round(sqrt((v1(1)-v2(1))^2 + (v1(2)-v2(2))^2)/speed/T);
    count2 = round(sqrt((v2(1)-v3(1))^2 + (v2(2)-v3(2))^2)/speed/T);
    count = count1+count2;
    
    % generate trajectory points
    points = [linspace(v1(1), v2(1), count1)', linspace(v1(2), v2(2), count1)', zeros(count1,1)];
    points = [points; linspace(v2(1), v3(1), count2)', linspace(v2(2), v3(2), count2)', zeros(count2,1)];
end

function [points, count] = W(speed, D, T, center)
    % define verticies
    v1 = center + [D/2*cosd(135), D/2*sind(135), 0];
    v2 = center + [D/2*cosd(240), D/2*sind(240), 0];
    v3 = center;
    v4 = center + [D/2*cosd(300), D/2*sind(300), 0];
    v5 = center + [D/2*cosd(45), D/2*sind(45), 0];
    
    % calculate num_points
    count1 = round(sqrt((v1(1)-v2(1))^2 + (v1(2)-v2(2))^2)/speed/T);
    count2 = round(sqrt((v2(1)-v3(1))^2 + (v2(2)-v3(2))^2)/speed/T);
    count3 = round(sqrt((v3(1)-v4(1))^2 + (v3(2)-v4(2))^2)/speed/T);
    count4 = round(sqrt((v4(1)-v5(1))^2 + (v4(2)-v5(2))^2)/speed/T);
    count = count1+count2+count3+count4;
    
    % generate trajectory points
    points = [linspace(v1(1), v2(1), count1)', linspace(v1(2), v2(2), count1)', zeros(count1,1)];
    points = [points; linspace(v2(1), v3(1), count2)', linspace(v2(2), v3(2), count2)', zeros(count2,1)];
    points = [points; linspace(v3(1), v4(1), count3)', linspace(v3(2), v4(2), count3)', zeros(count3,1)];
    points = [points; linspace(v4(1), v5(1), count4)', linspace(v4(2), v5(2), count4)', zeros(count4,1)];
end

function [points, count] = seven(speed, D, T, center)
    % define verticies
    v1 = center + [D/2*cosd(120), D/2*sind(120), 0];
    v2 = center + [D/2*cosd(60), D/2*sind(60), 0];
    v3 = center + [D/2*cosd(270), D/2*sind(270), 0];
    
    % calculate num_points
    count1 = round(sqrt((v1(1)-v2(1))^2 + (v1(2)-v2(2))^2)/speed/T);
    count2 = round(sqrt((v2(1)-v3(1))^2 + (v2(2)-v3(2))^2)/speed/T);
    count = count1+count2;
    
    % generate trajectory points
    points = [linspace(v1(1), v2(1), count1)', linspace(v1(2), v2(2), count1)', zeros(count1,1)];
    points = [points; linspace(v2(1), v3(1), count2)', linspace(v2(2), v3(2), count2)', zeros(count2,1)];
end

function [points, count] = one(speed, D, T, center)
    % define verticies
    v1 = center + [D/2*cosd(90), D/2*sind(90), 0];
    v2 = center + [D/2*cosd(270), D/2*sind(270), 0];
    
    % calculate num_points
    count1 = round(sqrt((v1(1)-v2(1))^2 + (v1(2)-v2(2))^2)/speed/T);
    count = count1;
    
    % generate trajectory points
    points = [linspace(v1(1), v2(1), count1)', linspace(v1(2), v2(2), count1)', zeros(count1,1)];
end

function [points, count] = eight(speed, D, T, center)
% D = diameter
% T = sampling rate
    
    center1 = center + [0, D/4, 0];
    center2 = center + [0, -D/4, 0];

    % length of trajectory
    circumference = pi*D/2;
    
    % define number of points
    time = circumference/speed;
    count = round(time/T);

    % generate trajectory points
    t = linspace(0,1,count)';
    theta1 = t*(2*pi/t(end))-pi/2;
    theta2 = t*(2*pi/t(end))+pi/2;
    points = center1 + D/4*[cos(theta1) sin(theta1) zeros(size(theta1))];
    points = [points; center2 + D/4*[cos(theta2) sin(theta2) zeros(size(theta2))]];
    count = 2*count;
end

function [points, count] = four(speed, D, T, center)
% D = diameter
% T = sampling rate
    
    % define verticies
    v1 = center + [D/2*cosd(90), D/2*sind(90), 0];
    v2 = center + [D/2*cosd(180), D/2*sind(180), 0];
    v3 = center;
    v4 = center + [D/2*cosd(270), D/2*sind(270), 0];
    
    % calculate num_points
    count1 = round(sqrt((v1(1)-v2(1))^2 + (v1(2)-v2(2))^2)/speed/T);
    count2 = round(sqrt((v2(1)-v3(1))^2 + (v2(2)-v3(2))^2)/speed/T);
    count3 = round(sqrt((v3(1)-v4(1))^2 + (v3(2)-v4(2))^2)/speed/T);
    count = count1+count2+count3;
    
    % generate trajectory points
    points = [linspace(v1(1), v2(1), count1)', linspace(v1(2), v2(2), count1)', zeros(count1,1)];
    points = [points; linspace(v2(1), v3(1), count2)', linspace(v2(2), v3(2), count2)', zeros(count2,1)];
    points = [points; linspace(v3(1), v4(1), count3)', linspace(v3(2), v4(2), count3)', zeros(count3,1)];   

end

function [points, count] = five(speed, D, T, center)
% D = diameter
% T = sampling rate
    
    % define verticies
    v1 = center + [D/2*cosd(60), D/2*sind(60), 0];
    v2 = center + [D/2*cosd(120), D/2*sind(120), 0];
    v3 = center + [D/2*cosd(120), D/2*sind(0), 0];
    v4 = center + [D/2*cosd(60), D/2*sind(0), 0];
    v5 = center + [D/2*cosd(300), D/2*sind(300), 0];
    v6 = center + [D/2*cosd(240), D/2*sind(240), 0];
    
    % calculate num_points
    count1 = round(sqrt((v1(1)-v2(1))^2 + (v1(2)-v2(2))^2)/speed/T);
    count2 = round(sqrt((v2(1)-v3(1))^2 + (v2(2)-v3(2))^2)/speed/T);
    count3 = round(sqrt((v3(1)-v4(1))^2 + (v3(2)-v4(2))^2)/speed/T);
    count4 = round(sqrt((v4(1)-v5(1))^2 + (v4(2)-v5(2))^2)/speed/T);
    count5 = round(sqrt((v5(1)-v6(1))^2 + (v5(2)-v6(2))^2)/speed/T);
    count = count1+count2+count3+count4+count5;
    
    % generate trajectory points
    points = [linspace(v1(1), v2(1), count1)', linspace(v1(2), v2(2), count1)', zeros(count1,1)];
    points = [points; linspace(v2(1), v3(1), count2)', linspace(v2(2), v3(2), count2)', zeros(count2,1)];
    points = [points; linspace(v3(1), v4(1), count3)', linspace(v3(2), v4(2), count3)', zeros(count3,1)];   
    points = [points; linspace(v4(1), v5(1), count4)', linspace(v4(2), v5(2), count4)', zeros(count4,1)];
    points = [points; linspace(v5(1), v6(1), count5)', linspace(v5(2), v6(2), count5)', zeros(count5,1)];  
end