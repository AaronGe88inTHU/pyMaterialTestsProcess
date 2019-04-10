function [fitresult, gof] = FitMMC(x, y, z)
%FitMMC 此处显示有关此函数的摘要
% Von Mises屈服条件下的MMC模型 
% Ref. Application of extended Mohr–Coulomb criterion to ductile fracture
%global n;
global A;
[xData, yData, zData] = prepareSurfaceData(x, y, z );

% Set up fittype and options.

ft = @(c1,c2,n, x, y)((A/c2 .* (sqrt((1+c1^2)/3) .* cos(y.*pi/6)+c1 .* (x + 1/3.*sin(y.*pi/6)))) .^ (-1/n));
opts = fitoptions( 'Method', 'NonlinearLeastSquares' );
opts.Display = 'off';
opts.StartPoint = [0.1, 800, 0.1];
% Fit model to data.
[fitresult, gof] = fit( [xData, yData], zData, ft, opts );

end

