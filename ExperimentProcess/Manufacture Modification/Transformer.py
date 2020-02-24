import numpy as np
from scipy import optimize, interpolate
import pandas as pd
import matplotlib.pyplot as plt

def transform(p, x, y):
    #TODO: Read the xlsx files of origin tests of all rates and the formed sheet test at lowest rate
    if np.max(x[:,0]) >= np.max(y[:, 0]):
        trs =  interpolate.interp1d(p[0]+x[:,0], p[1]+x[:,1], bounds_error=False, fill_value=0)
        res = trs(y[:,0])
    else:
        trs =  interpolate.interp1d(-p[0]+y[:,0], -p[1]+y[:,1], bounds_error=False, fill_value=0)
        res = trs(x[:,0])
    return res

def read_files(origin_xlsx, formed_xlsx):
    #TODO: Read the xlsx files of origin tests of all rates and the formed sheet test at lowest rate
    
    origin = pd.ExcelFile(origin_xlsx)
    formed = pd.ExcelFile(formed_xlsx)
    
    origin_names = sorted(origin.sheet_names, key=lambda x: float(x))
    #curves = pd.read_excel("220.xlsx").values

    #print(origin_names)

    original_all = {}
    for name in origin_names:
        original_all[name] = (pd.read_excel(origin, name).values)
    #original = pd.read_excel(origin_xlsx, origin_names[0]).values
    # #print(original)
    formed = pd.read_excel(formed, 0).values   # formed_copy = formed.copy()
    # #print(formed)
    # #original = np.array(list(filter(lambda x: not np.isnan(x[1]), original)))
    
    # #neck = np.argmax(original[:,-1])
    # #original = original[:neck,:]
    # #original = np.array(list(filter(lambda x: x[0]>0.002, original)))
    # #print(original.shape)
    return  original_all, formed

def transform_low_rate(original, formed):
   
    neck_original= np.argmax(original[:,-1])
    original_neck = original[neck_original, 0]
    
    #original_copy = original.copy()

    formed = np.array(list(filter(lambda x: not np.isnan(x[1]), formed)))
    #neck_form = np.argmax(formed[:,-1])
    #print(neck_form)
    #failure = formed.shape[0]
    #formed = formed[:neck_form,:]
    formed = np.array(list(filter(lambda x: x[0]>0.01, formed)))
    form_neck = formed[-1, 0]
    #print(form_neck)
    diff = form_neck - original_neck
    #print(form_neck, original_neck)

    #print(formed.shape)


    def error_trs(p, x, y):
        """
        """
        trs = transform(p, x, y)
        #print(trs)
        #count = trs.shape[0]
        return trs-y[:, 1]

    #def scale(x, a):
    #    return a + x
   
    res = optimize.least_squares(error_trs, [diff,0],  args=(original, formed))
    
    #original_copy[:,0] = original_copy[:,0] + res1.x
    
    #res2=optimize.curve_fit(scale, transed[:, 1], formed[:,1])
    #print(res2[0])
    return res
def transform_all(original_all, res, coef, E = 210000):
    #TODO:
    outputs = {}
    for (rate, curve) in original_all.items():       
        #transed = np.array([formed[:, 0], transform(res.x, original, formed)]).T
        output = np.hstack([np.array(curve[:,0] + res.x[0]).reshape(-1,1), np.array(curve[:, 1]+ res.x[1] * (1 + coef * np.log(float(rate) / 0.001))).reshape(-1,1)])
        
        output_index = np.where(output[:,0] >= 0)
        output = output[output_index,:].reshape(-1,2)
        
        Elastic = E * output[:,0]
        
        temp = np.hstack([output, Elastic.reshape(-1,1)])
        
        elastic_index = np.where(temp[:, 1] > temp[:, 2])
        #print(elastic_index)
        output[elastic_index, 1] = Elastic[elastic_index]
        
        outputs[rate] = output
        #print(output)
    return outputs

def output_to_excel(filnename, outpus):
    with pd.ExcelWriter(filnename) as writer:
        for k, v in outpus.items():
            df = pd.DataFrame(np.array(v))
            df.to_excel(writer, k)




# origin_all, formed = read_files('220.xlsx','220_formed.xlsx')

# sorted_keys = sorted(origin_all.keys(), key=lambda x: float(x))

# original = origin_all[sorted_keys[0]]

# res = transform_low_rate(original, formed)
# print(res.x)
# transed = np.array([formed[:, 0], transform(res.x, original, formed)]).T
# plt.plot(original[:, 0], original[:, 1],'k')
# plt.plot(formed[:, 0], formed[:, 1],'r')

# output = original[:,0] + res.x[0], original[:, 1]+res.x[1]
# #df = pd.DataFrame(np.array(output).T)
# #df.to_excel("500.xlsx")

# plt.plot(transed[:,0], transed[:,1])
# plt.plot(output[0], output[1],'b')

# outputs = transform_all(origin_all, res, 0)
# output_to_excel(outputs)

# plt.show()

    


