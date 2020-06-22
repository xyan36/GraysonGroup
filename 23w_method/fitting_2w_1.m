%define surface direction as y, perpendicular direction as x, follow
    %[2015] axes notation
%define k matrix and other parameters
%fname = '200228\200228_glass_R78_R1516_2w_measurement_5.csv';
fname = '200302\200302_glass_R65_R1817_2w_measurement_1.csv';
%fname = '200303\200303_glass_R43_R2019_2w_measurement_1.csv';
data = readtable(fname);
switch fname
    case '200228\200228_glass_R78_R1516_2w_measurement_5.csv'
        Rh = 39.75;
        Rt = 39.92;
        Vdc = 0.3861;
        Idc = Vdc / Rt;
        V1w = 0.4698;
    case '200302\200302_glass_R65_R1817_2w_measurement_1.csv'
        Rh = 40.20;
        Rt = 40.27;
        Vdc = 0.3882;
        Idc = Vdc / Rt;
        V1w = 0.4786;
    case '200303\200303_glass_R43_R2019_2w_measurement_1.csv'
        Rh = 38.86;
        Rt = 39.79;
        Vdc = 0.3841;
        Idc = Vdc / Rt;
        V1w = 0.4621;
    otherwise
        disp('invalid case');
end
Lh =  1.83e-3;%2.15e-3; %m %-------------estimated, need to check autocad
alpha = (0.002015 + 0.002005 + 0.001989 + 0.001988) / 4;
% Rh = 39.75;%38.86;%40.20;%39.75;
% Rt = 39.92;%39.79;%40.27;%39.92;
% Vdc = 0.3861;%0.3841;%0.3882;%0.3861;
% Idc = Vdc / Rt;
% V1w = 0.4698;%0.4621;%0.4786;%0.4698;

data.T2wX = data.modifiedX2 * Rh * Lh * sqrt(2) / (V1w^2 * Rt * alpha * Idc);
data.T2wY = data.modifiedY2 * Rh * Lh * sqrt(2) / (V1w^2 * Rt * alpha * Idc);
%data.T2wX = data.modifiedX2 * sqrt(2) / (Rt * alpha * Idc);
%data.T2wY = data.modifiedY2 * sqrt(2) / (Rt * alpha * Idc);
T2wcombo = [data.T2wX ; data.T2wY];
freqcombo = [data.freq; data.freq];
% fo = fitoptions('Method','NonlinearLeastSquares',...
%                'Lower',[0,0,0],...
%                'Upper',[10,10,10],...
%                'StartPoint',[1,1,1]);
ft = fittype( 'anisotropicT2w(x, sdetk, p0, gamma2)', 'problem', 'gamma2');
gamma2s = 0.8 : 0.001 : 0.9;
Fits = cell(1, length(gamma2s));
Gofs = cell(1, length(gamma2s));

for i = 1 : 1 : length(gamma2s)
    [f,gof] = fit( freqcombo, T2wcombo, ft, 'StartPoint', [1, 1], 'problem', gamma2s(i));
    Fits{i} = f;
    Gofs{i} = gof;
end
    
f2 = figure;
sdetks = zeros(1, length(gamma2s));
p0s = zeros(1, length(gamma2s));
for i = 1 : 1 : length(gamma2s)
    sdetks(i) = Fits{i}.sdetk;
    p0s(i) = Fits{i}.p0;
end
plot(gamma2s, sdetks, 'DisplayName', 'sdetk')
hold on
plot(gamma2s, p0s, 'DisplayName', 'p0')
hold off
legend('show')
ax = gca;
ax.XLabel.String = 'Value of gamma2';
ax.YLabel.String = 'Value of fitting parameter';

f1 = figure;
plot(freqcombo, T2wcombo,'b.', 'MarkerSize', 6)
hold on
y = anisotropicT2w(freqcombo, f.sdetk, f.p0, f.gamma2);
plot(data.freq, y(1:length(data.freq)), 'LineWidth', 1)
hold on
plot(data.freq, y(length(data.freq) + 1 : end), 'LineWidth', 1)
hold off
legend('data', 'real fit', 'imag fit')
ax = gca;
ax.XScale = 'log';
ax.XLabel.String = 'f(Hz)';
ax.YLabel.String = 'T2w(K)';
% fparam = [detk, p0];
% result = [fparam; confintf];
% str = sprintf('Coefficients (with 95%% confidence bounds):\ndetk = %0.3f, (%0.3f, %0.3f)\np0 = %0.3f, (%0.3f, %0.3f)', result(:));
% text(100, -0.05, str)
%saveas(f1,[fname(1:end-4),'_T2w_fit.jpg'])

