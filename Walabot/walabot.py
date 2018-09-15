import os
import matplotlib.pyplot as plt
import time
import numpy as np
import mpl_toolkits.mplot3d.axes3d as axes3d
import matplotlib.animation as animation
import WalabotAPI


class Walabot:
    """ Control the walabot sensor"""

    def __init__(self):
        self.wa = WalabotAPI
        self.wa.Init()
        self.wa.SetSettingsFolder()

    def connect(self):
        """ Wait until a connection to the walabot is established """
        connecting = True
        while connecting:
            try:
                self.wa.ConnectAny()
                connecting = False
            except self.wa.WalabotError as err:
                connecting = True
                print('Could not connect... retrying')
                time.sleep(1)

    def calibrate(self):
        self.wa.StartCalibration()
        while self.wa.GetStatus()[0] == self.wa.STATUS_CALIBRATING:
            self.wa.Trigger()

    def start(self):
        self.wa.Start()

    def stop(self):
        self.wa.Stop()
        self.wa.Disconnect()

    def setParameters(self, r, theta, phi, threshold, imgfilter):
        self.wa.SetProfile(self.wa.PROF_SENSOR)
        self.wa.SetArenaR(*r)
        self.wa.SetArenaTheta(*theta)
        self.wa.SetArenaPhi(*phi)
        self.wa.SetThreshold(threshold)
        self.wa.SetDynamicImageFilter(imgfilter)

    def getRawData(self):
        self.wa.Trigger()
        raster, X, Y, Z, power = self.wa.GetRawImage()
        return raster, X, Y, Z


class LivePlot:
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlabel(r'$x$')
        self.ax.set_ylabel(r'$y$')
        self.ax.set_zlabel(r'$z$')

    def animate(self, raw, interval=50):
        def wrapper():
            self.ax.clear()
            self.plot(*raw)
        animation.FuncAnimation(self.fig, wrapper, interval=interval)

    def plot(self, raster, rSize, tSize, pSize):
        r = raster[0]
        theta = raster[1]
        phi = raster[2]

        # Convert to cartesian coords
        x = r * np.sin(theta) * np.cos(phi)
        y = r * np.sin(theta) * np.sin(phi)
        z = r * np.cos(theta)

        self.ax.plot_surface(x, y, z, cmap=plt.cm.YlGnBu_r)

def plot(raster, rSize, tSize, pSize):
    r = raster[0]
    theta = raster[1]
    phi = raster[2]

    # Convert to cartesian coords
    x = r*np.sin(theta)*np.cos(phi)
    y = r*np.sin(theta)*np.sin(phi)
    z = r*np.cos(theta)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x, y, z, cmap=plt.cm.YlGnBu_r)

    ax.set_xlabel(r'$x$')
    ax.set_ylabel(r'$y$')
    ax.set_zlabel(r'$z$')

    plt.show()


def main():
    wlbt = Walabot()
    wlbt.connect()

    rParams = (10.0, 100.0, 2.0)
    tParams = (-20.0, 20.0, 10.0)
    pParams = (-45.0, 45.0, 2.0)
    threshold = 15
    imgfilter = WalabotAPI.FILTER_TYPE_NONE

    wlbt.setParameters(rParams, tParams, pParams, threshold, imgfilter)
    wlbt.start()

    raster, rSize, tSize, pSize = wlbt.getRawData()
    r = raster[0]
    theta = raster[1]
    phi = raster[2]
    # Convert to cartesian coords
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for i in range(10000):
        print(raster)
    # for i in range(10000):
    #     ax.clear()
    #     ax.plot_surface(x, y, z, cmap=plt.cm.YlGnBu_r)
    #     print('Plotting')
    #     plt.pause(0.05)

    plt.show()

    # render = LivePlot()
    #
    # for i in range(10000):
    #     raw = wlbt.getRawData()
    #     render.animate(raw)
    #     plt.pause(0.001)

    # raw = wlbt.getRawData()
    # render.animate(raw)
    # for i in range(10):
    #     time.sleep(1)

    #plot(*wlbt.getRawData())
    wlbt.stop()


if __name__ == '__main__':
    main()