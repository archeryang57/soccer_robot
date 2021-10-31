import numpy as np
import matplotlib
import matplotlib.pyplot as plt
# %matplotlib inline

# set up matplotlib
is_ipython = 'inline' in matplotlib.get_backend()
if is_ipython:
    from IPython import display

plt.ion()
plt.figure(figsize=(18, 3))

class UGV_model:
    def __init__(self, x0, y0, theta0, L, v0, T): # L:wheel base
        self.x = x0 # X
        self.y = y0 # Y
        self.theta = theta0 # headding
        self.l = L  # wheel base
        self.v = v0  # speed
        self.dt = T  # decision time periodic
    def update(self, vt, deltat):  # update ugv's state
        dx = self.v*np.cos(self.theta)
        dy = self.v*np.sin(self.theta)
        dtheta = self.v*np.tan(deltat)/self.l
        self.x += dx*self.dt
        self.y += dy*self.dt
        self.theta += dtheta*self.dt
        
    def plot_duration(self):
        plt.scatter(self.x, self.y, color='r')   
        plt.axis([0, 18, -3, 3])
        if is_ipython:
            display.clear_output(wait=True)
            display.display(plt.gcf())  

# set reference trajectory
refer_path = np.zeros((100, 2))
refer_path[:,0] = np.linspace(0, 18, 100)


plt.plot(refer_path[:,0], refer_path[:,1], '-.b', linewidth=5.0)
ugv = UGV_model(0, 0, 0, 2.86, 2.0, 0.1)
for i in range(1000):
    ugv.update(2.0, np.cos(i/5.0))
    ugv.plot_duration()
