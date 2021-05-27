close all; clear all; clc

% python output:  output += [[t,theta_d[0],theta[0],h_theta[0],omega_d[0],omega[0],alpha_d[0],alpha[0],
%                               theta_d[1],theta[1],h_theta[1],omega_d[1],omega[1],alpha_d[1],alpha[1],
%                               effort[0],HEBI_effort[0],output_effort[0]*cable_multiplier[0],fric_effort[0],damp_effort[0],PD_effort[0],
%                               effort[1],HEBI_effort[1],output_effort[1]*cable_multiplier[1],fric_effort[1],damp_effort[1],PD_effort[1]]]
        

data = csvread('PD_1.csv');

%% Forward kinematics

L1 = 0.27*100;
L2 = 0.48*100;

theta_d = [data(:,2), data(:,7)];
x_d = L1*cos(theta_d(:,1))+L2*cos(theta_d(:,1)+theta_d(:,2));
y_d = L1*sin(theta_d(:,1))+L2*sin(theta_d(:,1)+theta_d(:,2));

theta = [data(:,4), data(:,9)];
x = L1*cos(theta(:,1))+L2*cos(theta(:,1)+theta(:,2));
y = L1*sin(theta(:,1))+L2*sin(theta(:,1)+theta(:,2));

%% Shape

figure()
plot(x_d, y_d, 'k--', 'Linewidth', 1.5); grid off; hold on; axis equal;
% plot(x, y, 'b', 'Linewidth', 1.5); 
% legend('Desired', 'PD')
ylim([0.6*100 0.75*100]); xlim([-0.08*100 0.08*100]);
xlabel('x [cm]');
ylabel('y [cm]');
set(gca,'units','centimeters')
set(gca,'xlimmode','manual','ylimmode','manual')
axpos = get(gca,'position');
set(gca,'position',[axpos(1:2) abs(diff(xlim)) abs(diff(ylim))])


print
print(gcf,'-dpng','-r0','star.png')
title('End Effector Position');