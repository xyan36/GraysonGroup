%%3w power dependence fit
%fname1 = '200309\200309_glass_R56_3w_measurement_1.txt';
%fname2 = '200406\200406_glass_R65_3w_measurement_2.txt';
%fname2 = '200407\200407_glass_R43_3w_measurement_2.txt';
%fname1 = '200310\200310_glass_R43_3w_measurement_1.txt';
f3p4 = readtable('200416\200416_glass_R56_power_dep_f3p4.txt');
f15 =  readtable('200416\200416_glass_R56_power_dep_f15.txt');
f30 = readtable('200416\200416_glass_R56_power_dep_f30.txt');
f50 = readtable('200416\200416_glass_R56_power_dep_f50.txt');

Rname = 'R56';
%Rname = 'R43';
Re0 = 40.2;%38.86;%40.20; %3w_1 old value
L = 1.83e-3; %---- estimated --- #length between V1w contacts
alpha = (0.002015 + 0.002005 + 0.001989 + 0.001988) / 4;

freqs = [3.4, 15, 30, 50];

f3p4.I1w = f3p4.X1 / Re0;
f15.I1w = f15.X1 / Re0;
f30.I1w = f30.X1 / Re0;
f50.I1w = f50.X1 / Re0;

% f3p4.X3_pure = f3p4.X3 - f3p4.X3_ref;
% f15.X3_pure = f15.X3 - f15.X3_ref;
% f30.X3_pure = f30.X3 - f30.X3_ref;
% f50.X3_pure = f50.X3 - f50.X3_ref;
% 
% f3p4.Y3_pure = f3p4.Y3 - f3p4.Y3_ref;
% f15.Y3_pure = f15.Y3 - f15.Y3_ref;
% f30.Y3_pure = f30.Y3 - f30.Y3_ref;
% f50.Y3_pure = f50.Y3 - f50.Y3_ref;

f = table(f3p4,f15,f30,f50);
f6 = figure;
colors = ['b','g','r','c'];
p = zeros(4,2);
hold on
p(1,:) = polyfit(f{:,1}.I1w(5:end-2).^3,f{:,1}.X3(5:end-2),1);
x = [0; f{:,1}.I1w(5:end-2).^3];
h(1) = scatter(f{:,1}.I1w(5:end-2).^3,f{:,1}.X3(5:end-2), 'MarkerEdgeColor', colors(1), ...
    'DisplayName', sprintf('f = %0.1fHz',freqs(1)));
h(5) = plot(x, polyval(p(1,:),x), 'Color', colors(1));
str = sprintf(' X3 = (%0.3e) * I1w^3 + (%0.3e)', p(1,:));
text(1.5e-8, -10e-6, str)
for i = 2:width(f)
    p(i,:) = polyfit(f{:,i}.I1w(5:end-2).^3,f{:,i}.X3(5:end-2),1);
    h(i) = scatter(f{:,i}.I1w(5:end-2).^3,f{:,i}.X3(5:end-2), 'MarkerEdgeColor', colors(i), ...
    'DisplayName', sprintf('f = %0.1fHz',freqs(i)));
    x = [0; f{:,i}.I1w(5:end-2).^3];
    h(4 + i) = plot(x, polyval(p(i,:),x), 'Color', colors(i));
    str = sprintf(' X3 = (%0.3e) * I1w^3 + (%0.3e)', p(i,:));
    text(1.5e-8, (-12 + i * 2) * 1e-6, str)
end
hold off
legend(h([1,2,3,4]))
xlabel('I_{1w}^3(A)')
ylabel('V3w(V)')
title([Rname, ' I_{1w}^3 vs. V_{3w}'])
text(2e-8,-12e-6, 'X3')
%saveas(f6, [fsave, Rname, '_I_1w_vs_X3.jpg'])

offset =  mean(p(:,2)); %1.2724e-6