import numpy as np

def lerp(alpha, p_v1, p_v2):
    return p_v1 + alpha * (p_v2 - p_v1)

def normalize(v):
    norm=np.linalg.norm(v)
    if norm==0:
       return v
    return v/norm
