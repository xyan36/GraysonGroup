function y = anisotropicT3w(x,detk,p0)
%p0 = kxx / detk^2;
P = 1;
ampl = P / sqrt(detk);
b = 10e-6; %m
C= 2.11*10^6; %J/m^3K
r = 0.5772; %Euler constant
%qxx = @(w, kxx) sqrt(1i.*2.*w.*C./kxx);
%%low frequency limit
y = real(ampl/pi * (-0.5*log(b^2*2*2*pi*x*C*p0) + 3/2 - r - 1i*pi/4));
%Thigh = @(w) P./(2.*k(1,1).*b.*qxx(w));
end