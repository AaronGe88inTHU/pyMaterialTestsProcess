%tension/compression

%mu1=0.00832;
%a1=3.8027;
%mu2=-0.035427;
%a2=2.4725;
%mu3=0.06827;
%a3=0.8653;


% e_shear=linspace(0,0.5,100)+1;
% sigma_shear=mu1*(e_shear.^(a1-1)-e_shear.^(-1*a1-1))+mu2*(e_shear.^(a2-1)-e_shear.^(-1*a2-1))+mu3*(e_shear.^(a3-1)-e_shear.^(-1*a3-1));
% figure;
% plot(e_shear,sigma_shear);
% 
% 
% 
% 
% mu1_ten=0.00601;
% a1_ten=1.2619;
% mu2_ten=-0.03627;
% a2_ten=0.39074;
% mu3_ten=-0.0052;
% a3_ten=-1.4684;
% 
% e_ten=linspace(0,2.5,100)+1;
% sigma_ten=mu1_ten*(e_ten.^(a1_ten-1)-e_ten.^(-0.5*a1_ten-1))+mu2_ten*(e_ten.^(a2_ten-1)-e_ten.^(-0.5*a2_ten-1))+mu3_ten*(e_ten.^(a3_ten-1)-e_ten.^(-0.5*a3_ten-1));
% figure;
% plot(e_ten,sigma_ten);

function f=FunOgdenFitting_ten(x)
mu=[x(1),x(2),x(3)];
a=[x(4),x(5),x(6)];
testData=csvread('rubberTestTen.csv',2,0);
e_ten_test=testData(:,1);
sigma_ten_test=testData(:,2);


N=3;
%mu=[0.00601,-0.03627,-0.0052];
%a=[1.2619,0.39074,-1.4684];
sigma_ten_calc=0;

for (i=1:1:N)
    sigma_ten_calc=sigma_ten_calc+mu(i)*(e_ten_test.^(a(i)-1)-e_ten_test.^(-0.5*a(i)-1));    
end
% figure;
% plot(e_ten_test,sigma_ten_test,'r');
% hold on;
% plot(e_ten_test,sigma_ten_calc);

f=sum((sigma_ten_calc-sigma_ten_test).^2);

 %plot_ten([0.00601,-0.03627,-0.0052,1.2619,0.39074,-1.4684]);
end
