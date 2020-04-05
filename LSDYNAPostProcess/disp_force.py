from nodoutReader import nodoutReader
from secforReader import secforReader
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd


def disp_force(node_ids, sec_id, res_file=0):
    node_info = nodoutReader('nodout')
    assert len(node_ids) == 2
    assert len(sec_id) == 1
    exp = np.array([0,0]).reshape(-1, 2)
    if not res_file == 0:
        exp = pd.read_csv(res_file).value
    #print(node_info.keys())
    dx_1 = np.array(node_info[293]).reshape(-1, 12)
    dx_2 = np.array(node_info[4282]).reshape(-1,12)
    disp = np.abs(dx_1[:, 1]- dx_2[:, 1])
    #print(disp)

    node_info = secforReader('secforc')
    #print(node_info.keys())

    sec_force = np.abs(np.array(node_info[1]).reshape(-1,5)[:, 2])
    #print(sec_x)
    plt.plot(exp[:, 0], exp[:, 1])
    plt.scatter(disp, sec_force)
    plt.show()

disp_force([293, 4282], [1])