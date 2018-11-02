import numpy as np

def get_sigma(sig, theta):
    xx = np.cos(theta) ** 2 * sig
    yy = np.sin(theta) ** 2 * sig
    xy = np.sin(theta) * np.cos(theta) * sig
    return np.array([xx, yy, xy]).T

def F00(alpha, m = 8):
    a1, a2, a3, a4, a5, a6 = alpha[0:6]
    c1 = np.power(np.abs(a1 * 2/3 - a2 * (-1/3)), m)
    c2 = np.power(np.abs(a3 * 2/3 + 2 * a4 * (-1/3)), m)
    c3 = np.power(np.abs(2 * a5 * 2/3 + a6 * (-1/3)),m)
    return c1 + c2 + c3 - 2

def F90(alpha, y90, m=8):
    a1, a2, a3, a4, a5, a6 = alpha[0:6]
    c1 = np.power(np.abs(a1 * (-1/3)- a2 * (2/3)), m)
    c2 = np.power(np.abs(a3 * (-1/3) + 2 * a4 * (2/3)), m)
    c3 = np.power(np.abs(2 * a5 * (-1/3)+ a6 * (2/3)),m)
    return c1 + c2 + c3 - 2 * np.power(1/y90, m)

def F45(alpha, y45, m=8):
   a1, a2, a3, a4, a5, a6, a7, a8 = alpha
   k21 = 0.5 * (a1 - a2)
   k12 = (2 * a5 + a6 + a3 + 2 * a4) / 9
   k22 = (2 * a5 + a6 -a3 - 2* a4) / 3

   c1 = np.power(0.5 * np.sqrt(k21 ** 2 + 4 * a7 ** 2), m)
   c2 = np.power(np.abs(((3* k12 - np.sqrt(k22 ** 2 + 4 * a8 ** 2)) / 4)), m)
   c3 = np.power((3 * k12 + np.sqrt(k22 ** 2 + 4 * a8 ** 2))/4, m)
   return c1 + c2 + c3 - 2 * np.power(1 / y45, m)

def Fb(alpha, yb, m=8, beta = 1):
   a1, a2, a3, a4, a5, a6 = alpha[0:6]
   c1 = np.power(np.abs((-1/3) * a1 - (-1/3) * a2), m)
   c2 = np.power(np.abs((-1/3) * a3 + (-2/3) * a4), m)
   c3 = np.power(np.abs((-2/3) * a5 + (-1/3) * a6), m)
   return c1 + c2 + c3 - 2 * np.power(1 / yb, m)



def G00(alpha, r00, sig_div, m=8):
    f2s = phi_dev_s(alpha, sig_div, m)
    return (1-r00) * f2s[0] - (2 + r00) * f2s[1]
    

def G45(alpha, r45, y45, sigma, m=8):
    f2sig = phi_dev_sigma(alpha, sigma, m)
    return f2sig[0] + f2sig[1] - 2 * m / y45 / (1 +r45)


def G90(alpha, r90, s90, m=8):
    f2s = phi_dev_s(alpha, s90, m)
    return (2 + r90) * f2s[0] - (1-r90) * f2s[1]

def Gb(alpha, rb, sb, m=8):
    f2s = phi_dev_s(alpha, sb, m)
    return (1 + 2 * rb) * f2s[0] - (2 + rb) * f2s[1]

def get_delta(X):
    delta = (X[0] - X[1]) ** 2 + 4 * X[2] ** 2
    return delta



def phi1_dev_X1(X,m=8):
    xx, yy, xy = X[:]
    if xx == yy and xy == 0:
        return np.array([0,0,0])
    
    xp_1, xp_2 = principal(X)
    delta = get_delta(X)
    phi1_dev_xp1 = m * (xp_1 - xp_2) ** (m-1)
    phi1_dev_xp2 = -m * (xp_1 - xp_2) ** (m-1)

    
    xp1_dev_xx = 0.5 * (1 + (xx-yy) / np.sqrt(delta))
    xp2_dev_xx = 0.5 * (1 - (xx-yy) / np.sqrt(delta)) 

    xp1_dev_yy = 0.5 * (1 - (xx-yy) / np.sqrt(delta)) 
    xp2_dev_yy = 0.5 * (1 + (xx-yy) / np.sqrt(delta))

    xp1_dev_xy = 2 * xy / np.sqrt(delta)
    xp2_dev_xy = -2 * xy / np.sqrt(delta)

    c1 = phi1_dev_xp1 * xp1_dev_xx + phi1_dev_xp2 * xp2_dev_xx
    c2 = phi1_dev_xp1 * xp1_dev_yy + phi1_dev_xp2 * xp2_dev_yy
    c3 = phi1_dev_xp1 * xp1_dev_xy + phi1_dev_xp2 * xp2_dev_xy
    return np.array([c1, c2, c3])
    '''
    return phi1_dev_xp1, phi1_dev_xp2
    '''

def phi2_dev_X2(X, m=8):
    xx, yy, xy = X[:]
    
    
    xp_1, xp_2 = principal(X)
    
    phi2_dev_xp1 = m * np.abs(2 * xp_2  + xp_1) ** (m-1) * np.sign(2 * xp_2  + xp_1) +\
                    2 * m * np.abs(2 * xp_1 + xp_2) ** (m-1) * np.sign(2 * xp_1 + xp_2)
    
    phi2_dev_xp2 = 2 * m * np.abs(2 * xp_2 + xp_1) ** (m-1) * np.sign(2 * xp_2 + xp_1) +\
                m * np.abs(2 * xp_1 + xp_2) ** (m-1) * np.sign(2 * xp_1 + xp_2)
    
    if xx == yy and xy == 0:
        return np.array([phi2_dev_xp1, phi2_dev_xp2, 0])
    
    delta = get_delta(X)

    xp1_dev_xx = 0.5 * (1 + (xx-yy) / np.sqrt(delta))
    xp2_dev_xx = 0.5 * (1 - (xx-yy) / np.sqrt(delta)) 

    xp1_dev_yy = 0.5 * (1 - (xx-yy) / np.sqrt(delta)) 
    xp2_dev_yy = 0.5 * (1 + (xx-yy) / np.sqrt(delta))

    xp1_dev_xy = 2 * xy / np.sqrt(delta)
    xp2_dev_xy = -2 * xy / np.sqrt(delta)
    



    c1 = phi2_dev_xp1 * xp1_dev_xx + phi2_dev_xp2 * xp2_dev_xx
    c2 = phi2_dev_xp1 * xp1_dev_yy + phi2_dev_xp2 * xp2_dev_yy
    c3 = phi2_dev_xp1 * xp1_dev_xy + phi2_dev_xp2 * xp2_dev_xy
    return np.array([c1, c2, c3])
    '''
    return phi2_dev_xp1, phi2_dev_xp2
    '''


def xp_dev_xx_yy(S):
    xx, yy, xy = S
    c = np.sqrt((0.5 * (xx - yy)) ** 2 + xy ** 2)

    xp1_dev_xx = 0.5 * xx + 0.25 * (xx - yy) / c
    xp1_dev_yy = 0.5 * yy - 0.25 * (xx - yy) / c

    xp2_dev_xx = 0.5 * xx - 0.25 * (xx - yy) / c
    xp2_dev_yy = 0.5 * xx + 0.25 * (xx - yy) / c

    return xp1_dev_xx, xp1_dev_yy, xp2_dev_xx, xp2_dev_yy



def phi_dev_s(alpha, S, m = 8):
    L1, L2 = linear_transform(alpha)
    
    C1 = get_C(L1)
    C2 = get_C(L2)
    X1 = np.matmul(C1, S)
    X2 = np.matmul(C2, S)
    
    co1 = np.matmul(phi1_dev_X1(X1), C1)
    co2 = np.matmul(phi2_dev_X2(X2), C2)
    phi_dev = co1 + co2
    return phi_dev[0], phi_dev[1]

def phi_dev_sigma(alpha, Sigma, m = 8):
    L1, L2 = linear_transform(alpha)
    '''
    print('s:',S)
    C1 = get_C(L1)
    C2 = get_C(L2)

    '''
    X1 = np.matmul(L1, Sigma)
    X2 = np.matmul(L2, Sigma)
    
    co1 = np.matmul(phi1_dev_X1(X1), L1)
    co2 = np.matmul(phi2_dev_X2(X2), L2)
    phi_dev = co1 + co2
    return phi_dev[0], phi_dev[1]
    
def principal(X):
    xp_1 = 0.5 * (X[0] + X[1] + np.sqrt((X[0]-X[1]) ** 2 + 4 * X[2] ** 2))
    xp_2 = 0.5 * (X[0] + X[1] - np.sqrt((X[0]-X[1]) ** 2 + 4 * X[2] ** 2))
    return xp_1, xp_2

def get_C(L):
    b = np.linalg.inv(np.array([[2/3, -1/3, 0],
                            [-1/3, 2/3, 0],
                            [0,0,1]]))
    return np.matmul(L, b) 

    

#def yielding45(alpha, s45, s00, m = 8)
def linear_transform(alpha):
    a1, a2, a3, a4, a5, a6, a7, a8 = alpha[:]
    L1 = np.matmul(np.array([[2/3, 0, 0], 
                            [-1/3, 0, 0],
                            [0, -1/3, 0], 
                            [0, 2/3, 0], 
                            [0,0,1]]), 
                    np.array([[a1],[a2],[a7]]))

    LM1 = np.array([[L1[0,0], L1[1, 0], 0],
                    [L1[2, 0], L1[3, 0], 0],
                    [0, 0, L1[4,0]]])

    L2 = np.matmul(1 / 9 * np.array([[-2, 2, 8, -2, 0],
                                    [1, -4, -4, 4, 0],
                                    [4, -4, -4, 1, 0],
                                    [-2, 8, 2, -2, 0],
                                    [0, 0, 0, 0 ,9]]),
                            np.array([[a3], [a4], [a5], [a6], [a8]]))
    LM2 = np.array([[L2[0,0], L2[1, 0], 0],
                    [L2[2, 0], L2[3, 0], 0],
                    [0, 0, L2[4,0]]])
    return LM1, LM2