from geometry import surface_area_hitmiss, surface_area_exact, pip_cn, pip_wn, pip_path
from mc_tools import Configuration, vis_bias, vis_MSE, vis_RMSE
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
    
def test_polygon2():
    p_vs = [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]]
    p_vs = [np.array(v) for v in p_vs]
    mean = surface_area_exact(p_vs)
    window = [0.0, 5.0, 0.0, 5.0]
    return p_vs, mean, window
    
def test(exp=10):
    p_vs, mean, window = test_polygon1()
    
    config = Configuration()
    config.nb_samples = [2**i for i in range(1, exp+1)]
    
    def f_cn(s):   return surface_area_hitmiss(f=pip_cn,   p_vs=p_vs, r=window, samples=s, plot=False)
    def f_wn(s):   return surface_area_hitmiss(f=pip_wn,   p_vs=p_vs, r=window, samples=s, plot=False)
    def f_path(s): return surface_area_hitmiss(f=pip_path, p_vs=p_vs, r=window, samples=s, plot=False)
    
    for f in [f_cn, f_wn, f_path]:
        vis_MSE( f=f, mean=mean, config=config)
        vis_RMSE(f=f, mean=mean, config=config)
        
def test_border():
    p_vs, mean, window = test_polygon2()
    
    vertices = [np.array([0.0, 0.0]), np.array([1.0, 0.0]), np.array([1.0, 1.0]), np.array([0.0, 1.0])]
    edges    = [np.array([0.0, 0.5]), np.array([1.0, 0.5]), np.array([0.5, 0.0]), np.array([1.0, 0.5])]
    
    for p in (vertices + edges):
        print('Point [{0}, {1}]\t cn={2}\t wn={3}\t path={4}'.format(p[0], p[1], pip_cn(p, p_vs), pip_wn(p, p_vs), pip_path(p, p_vs)))