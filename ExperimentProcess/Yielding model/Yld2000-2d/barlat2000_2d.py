import numpy as np
from scipy.optimize import least_squares
from opt_process import func_7_parameters, func_8_parameters
from yielding import get_sigma



y45 = 0.942
y90 = 0.960
yb = 1.013

#ys = {0:y0, 45:y45, 90:y90, 'b':yb}
r0 = 0.404
r45 = 0.699
r90 = 0.543
rb = 0.6

sigma_0 = get_sigma(1, 0)
sigma_45 = get_sigma(y45, np.pi/4)
print(sigma_45)
sigma_90 = get_sigma(y90, np.pi/2)
sigma_b = np.array([yb, yb, 0]).T

t = np.array([[2/3, -1/3, 0],
            [-1/3,2/3,0],
            [0,0,1]])
            
sig_div_0 = np.matmul(t, sigma_0)
sig_div_90 = np.matmul(t, sigma_90)
sig_div_b = np.matmul(t, sigma_b)
alpha = np.ones([8,])

res_1 = least_squares(func_7_parameters, alpha, args=[r0, sig_div_0, r45, y45, sigma_45, r90, y90, sig_div_90])
print(res_1.x)
res_2 = least_squares(func_8_parameters, alpha, args=[r0, sig_div_0, r45, y45, sigma_45,\
                                                    r90, y90, sig_div_90, rb, yb, sig_div_b])
print(res_2.x)