from math_utils import lerp
import numpy as np
from plotter import Plotter2D

###############################################################################
## Point Inside Polygon
###############################################################################
# Edge Crossing Rules:
# Rule 1: an upward edge includes its starting endpoint, and excludes its final endpoint;
# Rule 2: a downward edge excludes its starting endpoint, and includes its final endpoint;
# Rule 3: horizontal edges are excluded
# Rule 4: the edge-ray intersection point must be strictly right of the point P.

# (c) Sunday and Franklin [http://geomalgorithms.com/a03-_inclusion.html]
def pip_cn(p, p_vs):
    # Crossing number counter
    cn = 0
    p_v1 = p_vs[-1]
    for j in range(len(p_vs)):
		p_v2 = p_vs[j]
		# Upward crossing (Rule 1) or downward crossing (Rule 2)
		if (p_v1[1] <= p[1] and p[1] < p_v2[1]) or (p_v1[1] > p[1] and p[1] >= p_v2[1]):
		   # Lerp
		   alpha = (p[1] - p_v1[1]) / (p_v2[1] - p_v1[1])
		   # (Rule 4)
		   if p[0] < lerp(alpha, p_v1[0], p_v2[0]):
			   cn += 1
		p_v1 = p_v2
    # even = out, odd = in
    return bool(cn & 1)

# (c) Sunday [http://geomalgorithms.com/a03-_inclusion.html]
def pip_wn(p, p_vs):
    # >0 (left), =0 (on), <0 (right)
    def is_left(a, b):
        return (b[0] - a[0]) * (p[1] - a[1]) - (p[0] -  a[0]) * (b[1] - a[1])

    # Winding number counter
    wn = 0
    p_v1 = p_vs[-1]
    for p_v2 in p_vs:
        if p_v1[1] <= p[1]:
            # Upward crossing (Rule 1) with P to the left
            if (p[1] < p_v2[1]) and (is_left(p_v1, p_v2) > 0):
                wn += 1
        else:
            # Downward crossing (Rule 2) with P to the right
            if (p[1] >= p_v2[1]) and (is_left(p_v1, p_v2) < 0):
				wn -= 1
		p_v1 = p_v2
    return bool(wn)

from matplotlib.path import Path
def pip_path(p, p_vs):
    return Path(np.concatenate([p_vs, [p_vs[0]]])).contains_point(p)

###############################################################################
## Surface Area
###############################################################################
def surface_area_hitmiss(f, p_vs, r=None, samples=1000, rng=np.random, plot=True, plotter=None):
    if r is None:
        r = reduce(lambda acc, v: [min(acc[0], v[0]), max(acc[1], v[0]), min(acc[2], v[1]), max(acc[3], v[1])], p_vs, [np.inf, -np.inf, np.inf, -np.inf])
    window_x = (r[1] - r[0])
    window_y = (r[3] - r[2])

    if plot and plotter is None:
        plotter = Plotter2D()
    if plot:
        plotter.plot_AABB([r[0], r[2]], [r[1], r[3]], color='k')
        plotter.plot_contour(p_vs, color='b')

    p_in = 0
    for _ in range(samples):
        p = rng.random((2))
        p[0] = p[0] * window_x + r[0]
        p[1] = p[1] * window_y + r[2]
        if f(p, p_vs):
            p_in += 1
            color='g'
        else:
            color='r'
        if plot:
            plotter.plot_point(p, color=color)

    return float(p_in) / samples * (window_x * window_y)

def surface_area_exact(p_vs):
    area = 0.0
    nb_p_vs = len(p_vs)
    for j in range(nb_p_vs):
        p_v1 = p_vs[(j+nb_p_vs-1) % nb_p_vs]
        p_v2 = p_vs[j]
        p_v3 = p_vs[(j+nb_p_vs+1) % nb_p_vs]
        area += p_v2[0] * (p_v3[1] - p_v1[1])
    return 0.5 * abs(area)
