import numpy as np
from scipy import optimize, interpolate
import pandas as pd
import matplotlib.pyplot as plt

curves = pd.read_excel("980.xlsx").values

original = curves[:,[0,1]]
#print(original)
formed = curves[:,[2,3]]
formed_copy = formed.copy()
#print(formed)
#original = np.array(list(filter(lambda x: not np.isnan(x[1]), original)))
original_copy = original.copy()
#neck = np.argmax(original[:,-1])
#original = original[:neck,:]
#original = np.array(list(filter(lambda x: x[0]>0.002, original)))
#print(original.shape)
neck_original= np.argmax(original[:,-1])
original_neck = original[neck_original, 0]

formed = np.array(list(filter(lambda x: not np.isnan(x[1]), formed)))
neck_form = np.argmax(formed[:,-1])
#print(neck_form)
failure = formed.shape[0]
#formed = formed[:neck_form,:]
formed = np.array(list(filter(lambda x: x[0]>0.01, formed)))
form_neck = formed[-1, 0]
#print(form_neck)
diff = form_neck - original_neck
#print(form_neck, original_neck)

#print(formed.shape)

def transform(p, x, y):
    """
    """
    trs =  interpolate.interp1d(p[0]+x[:,0], p[1]+x[:,1], bounds_error=False, fill_value=0)
    res = trs(y[:,0])
    return res

def error_trs(p, x, y):
    """
    """
    trs = transform(p, x, y)
    #print(trs)
    #count = trs.shape[0]
    return trs-y[:, 1]

#def scale(x, a):
#    return a + x

res1 = optimize.least_squares(error_trs, [diff,10],  args=(original, formed))
transed = np.array([formed[:, 0], transform(res1.x, original, formed)]).T
#original_copy[:,0] = original_copy[:,0] + res1.x
print(res1.x)
#res2=optimize.curve_fit(scale, transed[:, 1], formed[:,1])
#print(res2[0])

plt.plot(original[:, 0], original[:, 1],'k')
plt.plot(formed_copy[:, 0], formed_copy[:, 1],'r')
output = original_copy[:,0] + res1.x[0], original_copy[:, 1]+res1.x[1]
df = pd.DataFrame(np.array(output).T)
df.to_excel("500.xlsx")

#plt.plot(transed[:,0], transed[:,1])
plt.plot(output[0], output[1],'b')



plt.show()

    


