function [cos3Theta, thetaBar] = LodeAngle2Triaxiality(T)
%LodeAngle2Triaxiality �˴���ʾ�йش˺�����ժҪ
%   �˴���ʾ��ϸ˵��
cos3Theta = -27/2 * T .* (T .^2 - 1/3);
thetaBar = 1 - 2 / pi* acos(cos3Theta);
end

