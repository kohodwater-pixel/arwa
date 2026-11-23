"""Provisional geometric reconstruction of the Ahmed Emaar Holding mark.
Coordinates are in reference-board pixels (1920x1088 board), measured from a
gold-pixel mask of the cover logo (x 144-258, y 78-191)."""
import numpy as np

def L(x):  # the single diagonal that cuts the tops of all three bars
    return 121.1 - 0.86 * (x - 172.2)

def fit_cubic(pts):
    pts = np.array(pts, float)
    d = np.r_[0, np.cumsum(np.hypot(*np.diff(pts, axis=0).T))]
    t = d / d[-1]
    P0, P3 = pts[0], pts[-1]
    b0 = (1 - t) ** 3; b1 = 3 * (1 - t) ** 2 * t; b2 = 3 * (1 - t) * t ** 2; b3 = t ** 3
    A = np.c_[b1, b2]
    R = pts - np.outer(b0, P0) - np.outer(b3, P3)
    sol, *_ = np.linalg.lstsq(A, R, rcond=None)
    return P0, sol[0], sol[1], P3

def f(p):
    return f"{p[0]:.2f},{p[1]:.2f}"

def mark_paths():
    B = 191.0
    paths = []
    # bar 1
    x0, x1 = 170.3, 181.6
    paths.append(f"M{x0},{B} L{x0},{L(x0):.2f} L{x1},{L(x1):.2f} L{x1},{B} Z")
    # bar 2
    x0, x1 = 189.9, 200.5
    paths.append(f"M{x0},{B} L{x0},{L(x0):.2f} L{x1},{L(x1):.2f} L{x1},{B} Z")
    # bar 3 with the wedge cap overhanging the second gap
    x0, x1, tip, under = 210.3, 222.3, 202.2, 96.2
    paths.append(f"M{x0},{B} L{x0},{under} L{tip},{under} L{tip},{L(tip):.2f} L{x1},{L(x1):.2f} L{x1},{B} Z")
    # crossbar to the arc (protrudes slightly into the gap, as in the reference)
    paths.append("M207.6,136 L224,136 L224,146.2 L207.6,146.2 Z")
    # arc (bowl) - outer ellipse c(223,178) 35.1x42, inner c(223,176) 26.8x30
    paths.append("M223,136 A35.1,42 0 0 1 258.1,178 L258.1,191 L249.8,191 L249.8,176 A26.8,30 0 0 0 223,146 Z")
    # foot with diagonal end
    paths.append(f"M{x0},180.6 L234.3,180.6 L242,{B} L{x0},{B} Z")
    # swoosh crescent crossing bar 1
    up = [(144.3,190),(146.8,179.9),(149.8,174.5),(154.2,167.4),(158.8,162.6),(163.2,158.2),(169.2,153.8),(182.8,146.0),(186.5,146.0)]
    lo = [(186.5,153.6),(182.8,155.5),(169.2,162.4),(163.2,166.4),(158.8,170.0),(154.2,175.0),(149.8,181.4),(146.8,186.2),(144.3,190)]
    a = fit_cubic(up); b = fit_cubic(lo)
    paths.append(f"M{f(a[0])} C{f(a[1])} {f(a[2])} {f(a[3])} L188.3,149.2 L{f(b[0])} C{f(b[1])} {f(b[2])} {f(b[3])} Z")
    return paths

BBOX = (144.3, 78.0, 258.1, 191.0)
