import 
def J_C(x0, plastic_stress_curves):
    A, B, n, c = x0 
    sr = {}
    if '1' in plastic_stress_curves.keys():
        stress = plastic_stress_curves['1']
        plastic_strain = stress[:, 0]
        rate1 = stress[:, 1]
    else:
        k = [ k for k in plastic_stress_curves.keys()][0]
        plastic_strain = plastic_stress_curves[k][:, 0]
        rate1 = np.array(A + B * np.power(plastic_strain, n))

    print(plastic_strain, rate1)
    for r, _ in plastic_stress_curves.items():
        #try:
            sr[r] = np.hstack([plastic_strain.reshape(-1,1), (rate1 * (1 + c * np.log(float(r)))).reshape(-1,1)])

    return sr

def J_C_Model(x0, plastic_stress_curves):
    A, B, n, c = x0 
    #print(plastic_stress_curves.keys())
    if '1' in plastic_stress_curves.keys():
        stress = plastic_stress_curves['1']
        rate1 = stress[:, 1]
    else:
        k = [ k for k in plastic_stress_curves.keys()][0]
        plastic_strain = plastic_stress_curves[k][:, 0]
        rate1 = np.array(A + B * np.power(plastic_strain, n))

    err = []

    for r, s in plastic_stress_curves.items():
        #try:
            sr = rate1 * (1 + c * np.log(float(r)))
            assert len(s) == len(sr)
            err.extend(s[:, 1] - sr)
        #except Exception as identifier:
        #    pass
    #print(err)
    return np.array(err)