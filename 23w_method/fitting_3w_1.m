%define surface direction as y, perpendicular direction as x, follow
    %[2015] axes notation
%define k matrix and other parameters
fname = '200309\200309_glass_R78_3w_measurement_1.txt';
%fname = '200309\200309_glass_R56_3w_measurement_1.txt';
%fname = '200310\200310_glass_R43_3w_measurement_1.txt';
data = readtable(fname);
switch fname
    case '200309\200309_glass_R78_3w_measurement_1.txt'
        Re0 = 39.75;
        V1w = 67.95e-3;
        I1w = V1w / Re0;
        Rname = 'R78';
    case '200309\200309_glass_R56_3w_measurement_1.txt'
        Re0 = 40.20;
        V1w = 69.21e-3;
        I1w = V1w / Re0;
        Rname = 'R56';
    case '200310\200310_glass_R43_3w_measurement_1.txt'
        Re0 = 38.86;
        V1w = 66.86e-3;
        I1w = V1w / Re0;
        Rname = 'R43';
    otherwise
        disp('invalid case');
end
alpha = (0.002015 + 0.002005 + 0.001989 + 0.001988) / 4;
data.X3_pure = data.X3 - mean(data.X3_ref);
L = 2.15e-3; %---- estimated --- #length between V1w contacts
P = V1w^2 / Re0 / L; %power / unit length
data.T_avg = data.X3_pure / (-1/2 * alpha * V1w) / P;
C = 2.11e6;
b = 10e-6; %half heater line width
r = 0.5772;

% fo = fitoptions('Method','NonlinearLeastSquares',...
%                'Lower',[0,0,0],...
%                'Upper',[10,10,10],...
%                'StartPoint',[1,1,1]);

p = polyfit(log(data.Lockin1f),data.T_avg,1);
% plot(log(data.Lockin1f),data.T_avg,'b.')
% hold on
% plot(log(data.Lockin1f),p(1) * log(data.Lockin1f)+p(2))
% hold off
detk = (1 / (pi * -2 * p(1)))^2;

ft = fittype( 'anisotropicT3w(x,detk,p0)', 'problem','detk');
%ft = fittype('anisotropicT3w(x,ampl,p0)');
f = fit( data.Lockin1f, data.T_avg, ft, 'problem', detk, 'StartPoint', [1]);
%f = fit( data.Lockin1f, data.T_avg, ft, 'StartPoint', [1,1]);
p0 = f.p0;
confintf = confint(f);
% f1 = figure;
% plot(f, data.Lockin1f, data.T_avg)
% ax = gca;
% ax.XScale = 'log';
% ax.XLabel.String = 'f(Hz)';
% ax.YLabel.String = 'T3w(K)';
fparam = p0;
result = [fparam; confintf];
% str = sprintf('Coefficients (with 95%% confidence bounds):\np0 = %0.3f, (%0.3f, %0.3f)', result(:));
% text(100, -0.05, str)

size = 1.0e+03 * [0.0010, 0.0010, 1.2800, 0.6473];
f2 = figure('Position', size);
plot(log(data.Lockin1f), data.T_avg, 'b.')
hold on
plot(log(data.Lockin1f), polyval(p,log(data.Lockin1f)),'color','cyan', 'LineWidth', 0.5)
plot(log(data.Lockin1f), anisotropicT3w(data.Lockin1f, detk, f.p0), 'r', 'lineWidth', 1.5)
plot(log(data.Lockin1f), anisotropicT3w(data.Lockin1f, detk, 1/sqrt(detk)),'g', 'LineWidth', 1.5)
hold off
str = sprintf('kxx / detk = %0.3e, (%0.3e, %0.3e)', result(:));
text(5, 1, str)
str = sprintf('detk = %0.3f', detk);
text(6, 4, str)
legend('data', 'slope best fit', 'magnitude best fit', 'magnitude expected using kxx = kyy = sqrt(detk)', ...
'Location', 'northeastoutside')
xlabel('ln(f)')
ylabel('T(K)')
title([Rname, ' 3w slope and magnitude analysis'])
saveas(f2,[fname(1:end-4),'_T3w_slope_mag.jpg'])
