T =  [0,0.333, 0.39,.466];   
%thetaBar = [0.255,0.583, 0.458,0.515];
e_f =  [0.48,0.42, 0.412, 0.392];
[cos3Theta, thetaBar] = LodeAngle2Triaxiality(T);
%global n;
global A;
A = 1227;
%n = 0.136;

[fitresult,gof] = FitMMC(T, thetaBar,e_f);
fitresult
[xData, yData, zData] = prepareSurfaceData(T, thetaBar, e_f );
% Plot fit with data.
figure( 'Name', 'untitled fit 1' );
h = plot( fitresult, [xData, yData], zData );
hold on;
xx = linspace(-0.9, 0.9,50);
[a, yy] = LodeAngle2Triaxiality(xx);
zz = fitresult(xx, yy);
plot3(xx, yy, zz, 'k-');

xx = linspace(-0.666, .666,50);
yy=linspace(-0.666, .666,50);

[xData, yData] = meshgrid(xx, yy);
hold on;
zData = fitresult(xData, yData);

%thetaBar = 1 - 2 / pi* acos(cos3Theta);
y3Theta = cos((1-yData)/2 * pi);


surface(xData, yData, zData);
legend( h, 'untitled fit 1', 'e_f vs. T, thetaBar', 'Location', 'NorthEast' );
% Label axes
xlabel T
ylabel thetaBar
zlabel e_f
grid on
xlim([-1,1]);
ylim([-1,1]);
zlim([0,1]);

res = cat(3, y3Theta, xData, zData);