import numpy as np

strain_one_percent = np.arange(0, 0.01, 0.0001)
strain_to_one = np.arange(0.01, 1, 0.001)

five_to_twenty_per = np.arange(0.02, 0.301, 0.001)

zero_to_ten = np.arange(0, 10, 0.1)

strain_for_interlopating = np.hstack([strain_one_percent, strain_to_one, 1]).reshape(-1, 1)

#print(strain_for_interlopating)