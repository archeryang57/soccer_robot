import numpy as np

def clockwise_angle(v1, v2):
    x1,y1 = v1
    x2,y2 = v2
    dot = x1*x2+y1*y2
    det = x1*y2-y1*x2
    theta = np.arctan2(det, dot)
    theta = theta if theta>0 else 2*np.pi+theta
    return theta

v1 = [0, 1]
v2 = [1, 1]
theta = clockwise_angle(v1,v2)
theta = 360 - (theta*180/np.pi)
print(f"{theta}")