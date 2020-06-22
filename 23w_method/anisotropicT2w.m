function y = anisotropicT2w(x, sdetk, p0, gamma2)
%define surface direction as y, perpendicular direction as x, follow
    %[2015] axes notation
    gamma1 = 1;
    P = 1;
    L = 1;
    y = zeros(length(x),1);
    ampl = gamma2 * P / (L * sdetk);
    b = gamma1 * 10e-6;
    cv = 2.11e6;
    D = 50e-6;
    wt = 2 * b;
    wh = 2 * b;
    for i = 1:1:round(length(x) / 2)
    int_wt_wh = integral2(@(t,y0) ...
                besselk(0, sqrt(1j * 2 * 2 * pi * x(i) * cv) * abs(D + t - y0) / sqrt(p0)), ...
                -wt / 2, wt / 2, -wh / 2, wh / 2);
    %y(i) = real(P ./ (pi .* L .* sqrt(detk) .* wt .* wh) .* int_wt_wh);
    y(i) = real(ampl/ (pi * wt * wh) * int_wt_wh);
    end
    for i = round(length(x) / 2) + 1:1:length(x)
    int_wt_wh = integral2(@(t,y0) ...
                besselk(0, sqrt(1j * 2 * 2 * pi * x(i) * cv) * abs(D + t - y0) / sqrt(p0)), ...
                -wt / 2, wt / 2, -wh / 2, wh / 2);
    y(i) = imag(ampl/ (pi * wt * wh) * int_wt_wh);
    end
end
