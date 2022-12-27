
from PyQt5 import QtGui, QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QTabWidget
from modules import interface
from modules.displays import Display
import numpy as np
import math
from modules.utility import print_debug, print_log
import sys


class MainWindow(QtWidgets.QMainWindow):
    ''' This is the PyQt5 GUI Main Window'''
    arr=[]
    count=0
    a=[]

    def __init__(self, *args, **kwargs):
        ''' Main window constructor'''

        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('./resources/MainWindow.ui', self)

        # set the title and icon
        self.setWindowIcon(QtGui.QIcon('./resources/icons/icon.png'))
        self.setWindowTitle("Medical Image Viewer")

        self.disp = Display(self)

        # initialize ui connectors
        interface.init_connectors(self)
    def mouse_clicked_line(self, evt):

        vb = self.axial_box.plotItem.vb
        scene_coords = evt.scenePos()
        if self.axial_box.sceneBoundingRect().contains(scene_coords):
            mouse_point = vb.mapSceneToView(scene_coords)
            if self.count<2:
             print(f'clicked plot X: {mouse_point.x()}, Y: {mouse_point.y()}, event: {evt}') 
             self.arr.append(mouse_point.x())
             self.arr.append(mouse_point.y())
             
             
             print(self.arr)
             self.count=self.count+1
            if self.count==2: 
              self.dist(self.arr)
    def dist(self,arr):
        dist = math.sqrt( (arr[2] - arr[0])**2 + (arr[1] - arr[3])**2 )
        self.count=0
        self.arr=[]
        print("distance")
        print(dist)
        return dist
    def mouse_clicked_line_angle(self, evt):

        vb = self.sagittal_box.plotItem.vb
        scene_coords = evt.scenePos()
        if self.sagittal_box.sceneBoundingRect().contains(scene_coords):
            mouse_point = vb.mapSceneToView(scene_coords)
            if self.count<3:
             print(f'clicked plot X: {mouse_point.x()}, Y: {mouse_point.y()}, event: {evt}') 
             self.a.append(mouse_point.x())
             self.a.append(mouse_point.y())
             
             
             print(self.a)
             self.count=self.count+1
            if self.count==3: 
              self.angle3pt(self.a)
    def angle3pt(self,a):
     """Counterclockwise angle in degrees by turning from a to c around b
        Returns a float between 0.0 and 360.0"""
     ang = math.degrees(
     math.atan2(a[5]-a[3], a[4]-a[2]) - math.atan2(a[1]-a[3], a[0]-a[2]))
     self.count=0
     self.a=[]
     if ang<0:
        ang=ang+360
        print("angle")
        print(ang)
        return ang
     else:
        print("angle")
        print(ang)
        return ang   
     print("angle")
     
     return ang + 360 if ang < 0 else ang          
    

    def regionUpdated(self,regionItem):
     points=[]
     xarr=[]
     yarr=[]
     points= regionItem.getLocalHandlePositions() 
     for i in range (len(points)):
           point=points[i][1]
           print(point.x())
           xarr.append(point.x())
           yarr.append(point.y())
           #self.distt(xarr,yarr)

      
     
     self.distt(xarr,yarr)
     print("sssssssssssssssssss")
     


      #print(points.pop().split())
      #print(points) 
    def distt(self,x,y):
         dist = math.sqrt( (x[1] - x[0])**2 + (y[1] - y[0])**2 )
         print("distanceeeeeeeeeeeeee")
         print(dist)
         return dist

    
            
    

def main():

    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
