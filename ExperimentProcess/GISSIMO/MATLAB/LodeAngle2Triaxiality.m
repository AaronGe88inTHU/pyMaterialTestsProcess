function [cos3Theta, thetaBar] = LodeAngle2Triaxiality(T)
%LodeAngle2Triaxiality 此处显示有关此函数的摘要
%   此处显示详细说明
cos3Theta = -27/2 * T .* (T .^2 - 1/3);
thetaBar = 1 - 2 / pi* acos(cos3Theta);
end

