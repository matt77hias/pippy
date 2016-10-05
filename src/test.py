from geometry import surface_area_hitmiss, surface_area_exact, pip_cn, pip_wn, pip_path
from mc_tools import vis_bias, vis_MSE, vis_RMSE
import numpy as np

###################################################################################################################################################################################
## Test
################################################################################################################################################################################### 
def test_polygon1():
    p_vs = [[50.0, 150.0], [200.0, 50.0], [350.0, 150.0], [350.0, 300.0], [250.0, 300.0], [200.0, 250.0], [150.0, 350.0], [100.0, 250.0], [100.0, 200.0]]
    p_vs = [np.array(v) for v in p_vs]
    mean = surface_area_exact(p_vs)
    window = [0.0, 350.0, 0.0, 350.0]
    return p_vs, mean, window

def test(exp=10):
    nb_samples=[2**i for i in range(1, exp+1)]
    p_vs, mean, window = test_polygon1()
    
    def f_cn(s):   return surface_area_hitmiss(f=pip_cn,   p_vs=p_vs, r=window, samples=s, plot=False)
    def f_wn(s):   return surface_area_hitmiss(f=pip_wn,   p_vs=p_vs, r=window, samples=s, plot=False)
    def f_path(s): return surface_area_hitmiss(f=pip_path, p_vs=p_vs, r=window, samples=s, plot=False)
    
    for f in [f_wn, f_wn, f_path]: 
        vis_MSE(f=f, mean=mean, nb_samples=nb_samples)
        vis_RMSE(f=f, mean=mean, nb_samples=nb_samples)
        
