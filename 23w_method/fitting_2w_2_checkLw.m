%define surface direction as y, perpendicular direction as x, follow
    %[2015] axes notation
%define k matrix and other parameters
%fname = '200228\200228_glass_R78_R1516_2w_measurement_5.csv';
%fname = '200302\200302_glass_R65_R1817_2w_measurement_1.csv';
fname = '200303\200303_glass_R43_R2019_2w_measurement_1.csv';
data = readtable(fname);
%Lh =  1.85e-3; %m %-------------estimated, need to check autocad
alpha = (0.002015 + 0.002005 + 0.001989 + 0.001988) / 4;
Rh = 38.86;%38.86;%40.20;%39.75;
Rt = 39.79;%39.79;%40.27;%39.92;
Vdc = 0.3841;%0.3841;%0.3882;%0.3861;
Idc = Vdc / Rt;
V1w = 0.4621;%0.4621;%0.4786;%0.4698;

data.T2wX = data.modifiedX2 * Rh * sqrt(2) / (V1w^2 * Rt * alpha * Idc);
data.T2wY = data.modifiedY2 * Rh * sqrt(2) / (V1w^2 * Rt * alpha * Idc);
%data.T2wX = data.modifiedX2 * sqrt(2) / (Rt * alpha * Idc);
%data.T2wY = data.modifiedY2 * sqrt(2) / (Rt * alpha * Idc);
T2wcombo = [data.T2wX ; data.T2wY];
freqcombo = [data.freq; data.freq];
% fo = fitoptions('Method','NonlinearLeastSquares',...
%                'Lower',[0,0,0],...
%                'Upper',[10,10,10],...
%                'StartPoint',[1,1,1]);
ft = fittype( 'anisotropicT2w2(x,ampl,p0)');
f = fit( freqcombo, T2wcombo, ft, 'StartPoint', [1,1]);
%ampl = P / (L * sqrt(detk)) = V1w^2 / Rh / Lh / sqrt(detk)
ampl = f.ampl;
p0 = f.p0;
confintf = confint(f);
%detk = (V1w^2 / Rh / Lh / ampl)^2;
%detk = (1 / ampl)^2;
%f1 = figure;
plot(freqcombo, T2wcombo,'b.', 'MarkerSize', 6)
hold on
h = anisotropicT2w2(freqcombo,ampl,p0);
plot(data.freq, h(1:length(data.freq)), 'LineWidth', 1)
hold on
plot(data.freq, h(length(data.freq) + 1 : end), 'LineWidth', 1)
hold off
legend('data', 'real fit', 'imag fit')
ax = gca;
ax.XScale = 'log';
ax.XLabel.String = 'f(Hz)';
ax.YLabel.String = 'T2w(K)';
fparam = [ampl, p0];
result = [fparam; confintf];
str = sprintf('Coefficients (with 95%% confidence bounds):\ndetk = %0.3f, (%0.3f, %0.3f)\np0 = %0.3f, (%0.3f, %0.3f)', result(:));
text(100, -0.05, str)
%saveas(f1,[fname(1:end-4),'_T2w_fit.jpg'])

