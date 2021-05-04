import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class Bicycle():
    def __init__(self):
        self.xc = 0
        self.yc = 0
        self.theta = 0
        self.delta = 0
        self.beta = 0
        
        self.L = 2
        self.lr = 1.2
        self.w_max = 1.22
        
        self.sample_time = 0.01
        
    def reset(self):
        self.xc = 0
        self.yc = 0
        self.theta = 0
        self.delta = 0
        self.beta = 0

    def step(self, v, w):
        
        # ==================================
        #  Implement kinematic model here
        # ==================================
        
        self.xc=self.xc+self.sample_time*(v*np.cos(self.theta+self.beta))
        self.yc=self.yc+self.sample_time*(v*np.sin(self.theta+self.beta))
        self.theta=self.theta+self.sample_time*((v*np.cos(self.beta)*np.tan(self.delta))/self.L)
        self.delta=self.delta+self.sample_time*(w)
        self.beta=np.arctan(self.lr*np.tan(self.delta)/self.L)
    
    def circle_center_dist(self,a,b):
        #a,b, is the center of the circle
        d=(self.xc-a)*(self.xc-a)+(self.yc-b)*(self.yc-b)
        return d

def main():
    model = Bicycle()

    sample_time = 0.01
    time_end = 10
    model.reset()

    t_data = np.arange(0,time_end,sample_time)
    x_data = np.zeros_like(t_data)
    y_data = np.zeros_like(t_data)
    v_data = np.zeros_like(t_data)
    w_data = np.zeros_like(t_data)

    delta_data=np.zeros_like(t_data)

    v_data[:]=(32/30)*np.pi
    for i in range(t_data.shape[0]):
        x_data[i] = model.xc
        y_data[i] = model.yc
        model.beta=0
        
        if ((i>=375) and (i < 1875)):
            if model.circle_center_dist(16,8) > 64:
                w_data[i]=model.w_max
            elif model.circle_center_dist(16,8) < 64:
                w_data[i]=-model.w_max
            else:
                w_data[i]=0
            print(model.circle_center_dist(16,8),w_data[i])
        else:
            print(model.circle_center_dist(0,8))

            if model.circle_center_dist(0,8) > 64:
                w_data[i]=model.w_max
            elif model.circle_center_dist(0,8) < 64:
                w_data[i]=-model.w_max
            else:
                w_data[i]=0
            print(model.circle_center_dist(0,8),w_data[i])

        delta_data[i]=model.delta
        model.step(v_data[i], w_data[i])        

    plt.axis('equal')
    plt.plot(x_data, y_data)
    plt.show()
    print(x_data.shape)

if __name__ == "__main__":
    main()