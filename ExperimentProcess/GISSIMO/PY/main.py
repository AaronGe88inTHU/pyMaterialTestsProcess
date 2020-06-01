import glob
import os
from disp_force import *
from MMCTable import *
from matplotlib import pyplot as plt
from scipy.optimize import LinearConstraint, NonlinearConstraint, differential_evolution
from scipy.interpolate import interp1d
from dtw import *


cur_num = 0
def lookup_drop(curve):
    """
    TODO
    """
    load = curve[:, 1]
    diff = np.diff(load)
    maxx = np.max(load)
    idx = np.where(diff < -maxx/3)
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
def func_simulation(param, args):
    """
    TODO
    """
    
    k_file, punch = args

    writeGissimoCurve(param)
    #simu = []
    cmd =  "lsdyna.exe i="+k_file+" NCPU=8" 
    os.system(cmd)

    
    if punch:
        sim_curve = disp_force_rgdwall("punch")
    else:
        sim_curve = disp_force(k_file.split(".")[0], 0)
        
    fail = lookup_drop(sim_curve)
    
    f_simu = interp1d(sim_curve[:, 0], sim_curve[:, 1])
    z_to_fail = np.arange(0, fail, 0.01)
    simu = f_simu(z_to_fail)
    #simu.append(fail)
    # plt.plot(sim_curve[:,0], sim_curve[:,1])

    # plt.show()
    global cur_num
    cur_num += 1
    #print(cur_num)
    return simu

def err_func(param, args):
    #print(param)
    s1, s2 = param[0], param[1]
    simu = np.array(func_simulation([s1, s2, 1,1,1],))
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

def do_inverse(test, k_file, exp_file, punch = False):
    """
    TODO
    """
    res = 0

    #csv_files = glob.glob("*.csv")
    #csv_files.sort()
    #csv_f = [c.split('.')[0] for c in csv_files]

    #k_files = [glob.glob(c+"*.k") for c in csv_f]
    #k_files = np.sort(np.array(k_files).flatten())
    #func_simulation([-1, 1200])
    #try:
    constraint_1 = NonlinearConstraint(lambda x: x[0] - x[1], 0.01, np.inf)
	#constraint_2 = NonlinearConstraint(lambda x: x[0], 0.1, 1)
	#constraint_3 = NonlinearConstraint(lambda x: x[1], 0.05, np.inf)
	
    
    res = differential_evolution(err_func, bounds=([0.1, 1], [0.05, 0.5]), args=[test, k_file, exp_file, punch],constraints = (constraint_1, ))
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



res = do_inverse(test)
print(res)