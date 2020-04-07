import glob
import os
from disp_force import *
from MMCTable import *
from matplotlib import pyplot as plt

csv_files = glob.glob("*.csv")
csv_files.sort()
csv_f = [c.split('.')[0] for c in csv_files]

k_files = [glob.glob(c+"*.k") for c in csv_f]
k_files = np.sort(np.array(k_files).flatten())

#print(k_file)

A = 3043.18303
n = 0.12954
C, D = -1, 1800
E, F, G = 1, -1, 1
failureSurface = MMCSurface(A, n, np.exp(C), D)
writeTable(failureSurface)
eta, ercit = QuadCurve(E, F, G)
writeErcit(eta, ercit)

commands = ["lsdyna.exe i="+k+" NCPU=8" for k in k_files]

for cmd in commands:
    print(cmd)
    os.system(cmd)

for out, exp in zip(csv_f, csv_files):
    print(out)
    exp_curve = pd.read_csv(exp).values
    plt.scatter(exp_curve[:,0], exp_curve[:,1])
    sim_curve = disp_force(out, 0)
    plt.plot(sim_curve[:,0], sim_curve[:,1])

plt.show()

