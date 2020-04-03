function y = anisotropicT2w2(x,ampl,p0)
%define surface direction as y, perpendicular direction as x, follow
    %[2015] axes notation
    y = zeros(length(x),1);
    %ampl = L * sqrt(detk);
    w = 20e-6;
    cv = 2.11e6;
    D = 50e-6;
    for i = 1:1:round(length(x) / 2)
    int_wt_wh = integral2(@(t,y0) besselk(0, sqrt(1j * 2 * 2 * pi * x(i) * cv) * abs(D + t - y0) / sqrt(p0)), -w / 2, w / 2, -w / 2, w / 2);
    y(i) = real(1/ (pi * ampl * w^2) * int_wt_wh);
    end
    for i = round(length(x) / 2) + 1:1:length(x)
    int_wt_wh = integral2(@(t,y0) besselk(0, sqrt(1j * 2 * 2 * pi * x(i) * cv) * abs(D + t - y0) / sqrt(p0)), -w / 2, w / 2, -w / 2, w / 2);
    y(i) = imag(1/ (pi * ampl * w^2) * int_wt_wh);
    end
end
