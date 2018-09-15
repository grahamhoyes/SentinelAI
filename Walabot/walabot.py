import os
import matplotlib.pyplot as plt
import time
import numpy as np
import mpl_toolkits.mplot3d.axes3d as axes3d
import matplotlib.animation as animation
import matplotlib.gridspec as gridspec
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
        print('Starting calibration...')
        self.wa.StartCalibration()
        while self.wa.GetStatus()[0] == self.wa.STATUS_CALIBRATING:
            self.wa.Trigger()
        print('Calibration finished.')

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
        raster, x, y, z, power = self.wa.GetRawImage()
        energy = self.wa.GetImageEnergy()
        return raster, x, y, z, energy

    def getRawSlice(self):
        self.wa.Trigger()
        return self.wa.GetRawImageSlice()[0] # Only return the raster image


class LivePlot:
    def __init__(self):
        self.fig = plt.figure()

        self.ax1 = self.fig.add_subplot(121, projection='3d')
        self.ax1.set_xlabel(r'$x$')
        self.ax1.set_ylabel(r'$y$')
        self.ax1.set_zlabel(r'$z$')

        self.ax2 = self.fig.add_subplot(122)
        self.maxEnergy = 0

    def plot(self, raster, rSize, tSize, pSize, energy):

        r = raster[0]
        theta = raster[1]
        phi = raster[2]

        # Convert to cartesian coords
        x = r * np.sin(theta) * np.cos(phi)
        y = r * np.sin(theta) * np.sin(phi)
        z = r * np.cos(theta)

        self.maxEnergy = max(self.maxEnergy, energy)

        self.ax1.clear()
        self.ax2.clear()

        #self.ax1.plot_surface(x, y, z, cmap=plt.cm.YlGnBu_r)
        self.ax1.plot_wireframe(x, y, z, rstride=10, cstride=10)
        self.ax1.set_xlim([-255, 255])
        self.ax1.set_ylim([-255, 255])
        self.ax1.set_zlim([-255, 255])

        self.ax2.bar(1, energy, width=0.5)
        self.ax2.set_ylim([0, self.maxEnergy])
        plt.pause(0.001)

def main():
    wlbt = Walabot()
    wlbt.connect()

    rParams = (10.0, 100.0, 2.0)
    tParams = (-20.0, 20.0, 10.0)
    pParams = (-45.0, 45.0, 2.0)
    threshold = 15
    imgfilter = WalabotAPI.FILTER_TYPE_MTI

    wlbt.setParameters(rParams, tParams, pParams, threshold, imgfilter)
    wlbt.calibrate()
    wlbt.start()

    live = LivePlot()

    while True:
        live.plot(*wlbt.getRawData())

    # maxEnergy = 0.0
    # raster, rSize, tSize, pSize, energy = wlbt.getRawData()
    # theta = raster[0]
    # phi = raster[1]
    # r = raster[2]
    #
    # maxEnergy = max(energy, maxEnergy)
    # # Convert to cartesian coords
    # x = r * np.sin(theta) * np.cos(phi)
    # y = r * np.sin(theta) * np.sin(phi)
    # z = r * np.cos(theta)
    #
    # fig = plt.figure()
    # ax1 = fig.add_subplot(121, projection='3d')
    # ax1.set_xlim([0, 255])
    # ax1.set_ylim([0, 255])
    # ax1.set_zlim([0, 255])
    # ax2 = fig.add_subplot(122)
    # ax2.set_ylim([0, maxEnergy])

    # while True:
    #     ax1.clear()
    #     ax2.clear()
    #     raster, rSize, tSize, pSize, energy = wlbt.getRawData()
    #     theta = raster[0]
    #     phi = raster[1]
    #     r = raster[2]
    #     maxEnergy = max(energy, maxEnergy)
    #     # Convert to cartesian coords
    #     x = r * np.sin(theta) * np.cos(phi)
    #     y = r * np.sin(theta) * np.sin(phi)
    #     z = r * np.cos(theta)
    #     ax1.plot_surface(x, y, z, cmap=plt.cm.YlGnBu_r)
    #     ax1.set_xlim([-255, 255])
    #     ax1.set_ylim([-255, 255])
    #     ax1.set_zlim([-255, 255])
    #     ax2.bar(1, energy, width=0.5)
    #     ax2.set_ylim([0, maxEnergy])
    #     plt.pause(0.001)

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