"""
A demo P-controller.
"""

#from __future__ import input

from camera_feedback import CameraFeedback
from motor_control_ssc32 import Motors
import control_gui

import argparse
import ConfigParser
from threading import Thread, Event

# For logging
import time
from datetime import datetime
import csv

class Controller(Thread):
    """
    Controls the position of the ball on the platform.
    """
    
    def __init__(self, event, config_file, log = True, show = False):
        
        Thread.__init__(self)
        self.stopped = event
        
        self.cam = CameraFeedback(config_file, log = False)
        self.cam.show_on = show
        self.motors = Motors(config_file)
    
        ### Initialize controller variables ###
        # Should actually read these from the config file!
        config = ConfigParser.RawConfigParser()
        config.read(config_file)
        self.Td = config.getfloat('Controller','Td')
        self.K_x = -10
        self.Kd_x = -10
        self.K_y = -10
        self.Kd_y = -10
        
        self.x = [self.cam.x, self.cam.x]
        self.x_ref = [self.x[0]]
        self.y = [self.cam.y, self.cam.y]
        self.y_ref = [self.y[0]]
        self.ref_idx = 0
        self.e_x = [0, 0]
        self.e_y = [0, 0]
        self.phi_1 = [0,0]
        self.phi_2 = [0,0]
        
        self.__log_on = log
        if self.__log_on:
            self.log = True
            now_str = datetime.now().__str__().split('.')[0]
            now_str = now_str.replace(' ','-').replace(':','-')
            self.logfile = open(now_str + '_ctrl_log.csv','wb')
            self.logger = csv.writer(self.logfile,delimiter=';')
    
    def update(self):
        """
        This is one controller step.
        """
        
        # Update measurements
        (x,y) = self.cam.update()
        
        self.x.insert(0,x), self.x.pop()
        self.y.insert(0,y), self.y.pop()
        self.e_x.insert(0,self.x_ref[self.ref_idx]-x), self.e_x.pop()
        self.e_y.insert(0,self.y_ref[self.ref_idx]-y), self.e_y.pop()
        # Advance the reference index
        self.ref_idx = (self.ref_idx + 1) % min(len(self.x_ref), len(self.y_ref))
        
        # Control law
        self.phi_1.insert(0,0), self.phi_1.pop()
        self.phi_2.insert(0,0), self.phi_2.pop()
        self.phi_1[0] = self.K_x * self.e_x[0] + self.Kd_x * (self.e_x[0] - self.e_x[1]) / self.Td
        self.phi_2[0] = self.K_y * self.e_y[0] + self.Kd_y * (self.e_y[0] - self.e_y[1]) / self.Td
        self.motors.move(self.phi_1[0], self.phi_2[0])
        
        # Log data
        self.logger.writerow([time.time(),self.x[0],self.y[0],
                              self.x_ref[self.ref_idx], self.y_ref[self.ref_idx],
                              self.phi_1[0], self.phi_2[0]])
    
    def set_ref(self, x_ref, y_ref):
        """
        Set the reference position of the ball.
        x_ref and y_ref should be lists of the same size
        """
        self.x_ref = x_ref[:]
        self.y_ref = y_ref[:]
        self.ref_idx = 0
    
    def run(self):
        # Run update every Td
        while not self.stopped.wait(self.Td):
            self.update()
        
        self.__cleanup()
        
    def __cleanup(self):    
        self.cam.cleanup()
        self.motors.cleanup()
        if self.__log_on:
            self.logfile.close()
        
if __name__ == '__main__':

    # Parse command line arguments, if any
    parser = argparse.ArgumentParser(description='Ball position control, P control law')
    parser.add_argument('--config_file',help='Platform configuration file name',
                        default='platform.cfg')
    args = parser.parse_args()
    
    stop_flag = Event()
    ctrl = Controller(stop_flag, args.config_file, log=True, show = False)
    ctrl.start()
    
    gui = control_gui.ControlGui(ctrl)
    gui.run()
    
    stop_flag.set()
