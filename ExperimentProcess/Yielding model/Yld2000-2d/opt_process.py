import numpy as np
#from yielding import get_sigma
from yielding import G00, G45, G90, Gb, F00, F45, F90, Fb

def func_7_parameters(alpha, *args):
    r0, sig_div_0, r45, y45, sigma_45, r90, y90, sig_div_90 = args
    g00  = G00(alpha, r0, sig_div_0)
    f00 = F00(alpha)
    g45 = G45(alpha,r45, y45, sigma_45)
    f45 = F45(alpha, y45)
    g90 = G90(alpha, r90, sig_div_90 )
    f90 = F90(alpha, y90)
    #gb = Gb(alpha, rb, sig_div_b )
    #fb = Fb(alpha, yb)
    _, _, a3, _, _, a6, _, _= alpha
    #L12 = 1 * a3 - 4 * a4 - 4 * a5 + 4 * a6
    #L21 = 4 * a3 - 4 * a4 - 4 * a5 + a6  
    
    return np.array([g00, f00, g45, f45, g90, f90, a3-a6])

def func_8_parameters(alpha, *args):
    r0, sig_div_0, r45, y45, sigma_45, r90, y90, sig_div_90, rb, yb, sig_div_b = args
    g00  = G00(alpha, r0, sig_div_0)
    f00 = F00(alpha)
    g45 = G45(alpha,r45, y45, sigma_45)
    f45 = F45(alpha, y45)
    g90 = G90(alpha, r90, sig_div_90 )
    f90 = F90(alpha, y90)
    gb = Gb(alpha, rb, sig_div_b )
    fb = Fb(alpha, yb)
    #_, _, a3, _, _, a6, _, _= alpha
    #L12 = 1 * a3 - 4 * a4 - 4 * a5 + 4 * a6
    #L21 = 4 * a3 - 4 * a4 - 4 * a5 + a6  
    
    return np.array([g00, f00, g45, f45, g90, f90, gb, fb])