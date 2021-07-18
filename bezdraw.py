# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib import animation

# x1=10
# y1=80
# x2=50
# y2=10
# x3=90
# y3=80
# dots_num=100

# def two_degree_bc(x1=10, y1=80, x2=50, y2=10, x3=90, y3=80, dots_num=100): #bezier curve
#     global xt, yt, x_dots12, x_dots23, y_dots12, y_dots23
#     xt = []
#     yt = []
#     x_dots12 = np.linspace(x1, x2, dots_num)
#     y_dots12 = np.linspace(y1, y2, dots_num)
#     x_dots23 = np.linspace(x2, x3, dots_num)
#     y_dots23 = np.linspace(y2, y3, dots_num)
#     for i in range(dots_num):
#         x = x_dots12[i] + (x_dots23[i]-x_dots12[i])*i / (dots_num-1)
#         y = y_dots12[i] + (y_dots23[i]-y_dots12[i])*i / (dots_num-1)
#         xt.append(x)
#         yt.append(y)
  
  
# def run(i):
#     art1.set_data(x_dots12[i], y_dots12[i])
#     art2.set_data(x_dots23[i], y_dots23[i])
#     art3.set_data([x_dots12[i], x_dots23[i]], [y_dots12[i], y_dots23[i]])
#     art4.set_data(xt[i], yt[i])
#     return art1,art2,art3,art4


# two_degree_bc()
# fig, ax = plt.subplots(figsize=(8,8))
# ax.set_aspect(1)
# plt.xlim([0,100])
# plt.ylim([0,100])
# ax.plot([x1, x2], [y1, y2], color='#3e82fc')
# ax.plot([x2, x3], [y2, y3], color='#3e82fc')
# ax.plot(xt,yt,color='orange')
# art1, = ax.plot(x_dots12[0], y_dots12[0], color='green', marker='o') #scatter得到的对象不是一个list，是一个object
# art2, = ax.plot(x_dots23[0], y_dots23[0], color='green', marker='o') 
# art3, = ax.plot([x_dots12[0], x_dots23[0]], [y_dots12[0], y_dots23[0]], color = 'purple') #plot得到的结果是一个list，只包含一个元素，即一个形状object
# art4, = ax.plot(xt[0], yt[0], color='red', marker='o')
  
# ani = animation.FuncAnimation(
#     fig, run, frames=range(100), interval=20, blit=True, save_count=50)
# plt.show()


#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import math

from PyQt5 import QtGui, QtWidgets, QtCore


def binomial(i, n):
    """Binomial coefficient"""
    return math.factorial(n) / float(
        math.factorial(i) * math.factorial(n - i))


def bernstein(t, i, n):
    """Bernstein polynom"""
    return binomial(i, n) * (t ** i) * ((1 - t) ** (n - i))


def bezier(t, points):
    """Calculate coordinate of a point in the bezier curve"""
    n = len(points) - 1
    x = y = 0
    for i, pos in enumerate(points):
        bern = bernstein(t, i, n)
        x += pos[0] * bern
        y += pos[1] * bern
    return x, y


def bezier_curve_range(n, points):
    """Range of points in a curve bezier"""
    path=[]
    for i in range(n):
        t = i / float(n - 1)
        path.append(bezier(t, points))
    return path


class BezierDrawer(QtWidgets.QWidget):
    """Draw a Bezier Curve"""
  
    def __init__(self):
        super(BezierDrawer, self).__init__()

        self.setGeometry(300, 300, 450, 450)
        self.setWindowTitle('Bezier Curves')

    def paintEvent(self, e):
      
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHints(QtGui.QPainter.Antialiasing, True)
        self.doDrawing(qp)        
        qp.end()
        
    def doDrawing(self, qp):

        blackPen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.DashLine)
        redPen = QtGui.QPen(QtCore.Qt.red, 1, QtCore.Qt.DashLine)
        bluePen = QtGui.QPen(QtCore.Qt.blue, 1, QtCore.Qt.DashLine)
        greenPen = QtGui.QPen(QtCore.Qt.green, 1, QtCore.Qt.DashLine)
        redBrush = QtGui.QBrush(QtCore.Qt.red)

        # steps = 1000
        start_point = (200, 230)
        end_point = (400, 330)
        controlPoints = (
            start_point, 
            ((end_point[0]+start_point[0])/2, start_point[1]), 
            ((end_point[0]+start_point[0])/2, end_point[1]), 
            end_point)
        
        oldPoint = controlPoints[0]

        steps = max(abs(start_point[0]-end_point[0]), start_point[1]-end_point[1])

        # qp.setPen(redPen)
        # qp.setBrush(redBrush)
        # qp.drawEllipse(oldPoint[0] - 3, oldPoint[1] - 3, 6, 6)

        # qp.drawText(oldPoint[0] + 5, oldPoint[1] - 3, '1')
        # for i, point in enumerate(controlPoints[1:]):
        #     i += 2
        #     qp.setPen(blackPen)
        #     qp.drawLine(oldPoint[0], oldPoint[1], point[0], point[1])
            
        #     qp.setPen(redPen)
        #     qp.drawEllipse(point[0] - 3, point[1] - 3, 6, 6)

        #     qp.drawText(point[0] + 5, point[1] - 3, '%d' % i)
        #     oldPoint = point
            
        qp.setPen(bluePen)
        # for point in bezier_curve_range(steps, controlPoints):
        #     qp.drawLine(oldPoint[0], oldPoint[1], point[0], point[1])
        #     oldPoint = point
        path = bezier_curve_range(steps, controlPoints)
        oldPoint = path[0]
        for point in path:
            qp.drawLine(oldPoint[0], oldPoint[1], point[0], point[1])
            oldPoint = point


def main(args):
    app = QtWidgets.QApplication(sys.argv)
    ex = BezierDrawer()
    ex.show()
    app.exec_()


if __name__=='__main__':
    main(sys.argv[1:])