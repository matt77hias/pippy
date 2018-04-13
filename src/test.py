from geometry import surface_area_exact, surface_area_hitmiss, pip_cn, pip_wn, pip_path
from mc_tools import Configuration, vis_RMSE
import numpy as np

###############################################################################
## Test
############################################################################### 
def test_polygon1():
    p_vs = [[50.0, 150.0], [200.0, 50.0], [350.0, 150.0], [350.0, 300.0], [250.0, 300.0], [200.0, 250.0], [150.0, 350.0], [100.0, 250.0], [100.0, 200.0]]
    return [np.array(v) for v in p_vs]
    
def test_polygon2():
    p_vs = [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]]
    return [np.array(v) for v in p_vs]
    
def test(exp=12):
    p_vs = test_polygon1()
    exact = surface_area_exact(p_vs)
    
    config = Configuration()
    config.nb_samples = [2**i for i in range(1, exp+1)]
    
    def f_cn(s):   return surface_area_hitmiss(f=pip_cn,   p_vs=p_vs, samples=s, plot=False)
    def f_wn(s):   return surface_area_hitmiss(f=pip_wn,   p_vs=p_vs, samples=s, plot=False)
    def f_path(s): return surface_area_hitmiss(f=pip_path, p_vs=p_vs, samples=s, plot=False)
    
    for f in [f_cn, f_wn, f_path]:
        vis_RMSE(f=f, config=config, exact=exact)
        
def test_border():
    p_vs = test_polygon2()
    
    vertices = [np.array([0.0, 0.0]), np.array([1.0, 0.0]), np.array([1.0, 1.0]), np.array([0.0, 1.0])]
    edges    = [np.array([0.0, 0.5]), np.array([1.0, 0.5]), np.array([0.5, 0.0]), np.array([1.0, 0.5])]
    
    for p in (vertices + edges):
        print('Point [{0}, {1}]\t cn={2}\t wn={3}\t path={4}'.format(p[0], p[1], pip_cn(p, p_vs), pip_wn(p, p_vs), pip_path(p, p_vs)))
