import glob
import os
from disp_force import *
from MMCTable import *
from matplotlib import pyplot as plt
import scipy as sp
from scipy.optimize import LinearConstraint, NonlinearConstraint, differential_evolution, Bounds


cur_num = 0
def lookup_drop(curve):
    """
    TODO
    """
    load = curve[:, 1]
    diff = np.diff(load)
    maxx = np.max(load)
    idx = np.where(diff < -maxx/10)
    if len(idx[0]) == 0:
        ii = -2
    else:
        ii = idx[0][0]
    #print(load.shape, diff.shape)
    #print(idx[0])
    fail_point = curve[ii+1, 0]
    #print(fail_point)
    return fail_point

#print(k_file)
def func_simulation(param):
    """
    TODO
    """
    global cur_num

    #A = 3043.18303
    #n = 0.12954
    #C, D = param[0], param[1]
    #E, F, G = 1, -1, 1
    #failureSurface = MMCSurface(A, n, np.exp(C), D)
    #writeTable(failureSurface)
    #eta, ercit = QuadCurve(E, F, G)
    #writeErcit(eta, ercit)
    writeGissimoCurve(param)
    simu = []
    commands = ["lsdyna.exe i="+k+" NCPU=8" for k in k_files]

    for cmd in commands:
        print(cmd)
        os.system(cmd)

    for out in csv_f:
        #print(out)
        #exp_curve = pd.read_csv(exp).values
        #plt.scatter(exp_curve[:,0], exp_curve[:,1])
        #sim_curve = []
        #print(out)
        if out == "15":
            sim_curve = disp_force_rgdwall("15")
            
        else:
            sim_curve = disp_force(out, 0)
        
        fail = lookup_drop(sim_curve)
        simu.append(fail)
    # plt.plot(sim_curve[:,0], sim_curve[:,1])

    # plt.show()
    cur_num += 1
    #print(cur_num)
    return simu

def err_func(param, test):
    #print(param)
    s1, s2 = param[0], param[1]
    simu = np.array(func_simulation([s1, s2, 1,1,1]))
    res = test[0] - simu[0]
    res2 = np.sqrt(np.sum((np.power(res, 2))))
    #print(np.divide(test - simu, test[0]))
    global cur_num
    print(simu.shape)
    with open("shr.txt", "a+") as f:
        f.write("Iter: {}\n".format(cur_num))
        f.write("P: {}, {},\n".format(s1, s2))
        f.write("diff: {}, {}\n".format(res, res2))
    
    return res2

def do_inverse(test):
    """
    TODO
    """
    res = 0

    
    #try:
    constraint_1 = NonlinearConstraint(lambda x: x[0] - x[1], 0.01, np.inf)
	#constraint_2 = NonlinearConstraint(lambda x: x[0], 0.1, 1)
	#constraint_3 = NonlinearConstraint(lambda x: x[1], 0.05, np.inf)
	
    
    res = differential_evolution(err_func, bounds=([0.1, 1], [0.05, 0.5]), args=[test],constraints = (constraint_1, ))
        # reps_s1   0.299     
        # reps_s2   0.285     
        # reps_t    0.410     
        # reps_n    0.084     
        # reps_p    0.594   
        #print(res)
    #except ValueError as e:
        #print(res)
        #print('line 100')
        #print(str(e))

    return res




csv_files = glob.glob("*.csv")
csv_files.sort()
csv_f = [c.split('.')[0] for c in csv_files]

k_files = [glob.glob(c+"*.k") for c in csv_f]
k_files = np.sort(np.array(k_files).flatten())
#func_simulation([-1, 1200])

test = np.array([1.12])

res = do_inverse(test)
print(res)