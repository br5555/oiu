"""
A demo P-controller.
"""

#from __future__ import input

import camera_feedback
import motor_control_ssc32
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
        
        self.cam = camera_feedback.CameraFeedback(config_file, log = False)
        self.cam.show_on = show
        self.__motors = motor_control_ssc32.Motors(config_file)
    
        ### Initialize controller variables ###
        config = ConfigParser.RawConfigParser()
        config.read(config_file)
        self.Td = config.getfloat('Controller','Td')

        # Input variables
        self.e_trimf = [[-0.5, -0.15, -0.075],
                        [-0.15, -0.075, 0.0],
                        [-0.075, 0.0, 0.075],
                        [0.0, 0.075, 0.15],
                        [0.075, 0.15, 0.5]]
        
        self.de_trimf = [[-0.3, -0.1, -0.05],
                        [-0.1, -0.05, 0.0],
                        [-0.05, 0.0, 0.05],
                         [0.0, 0.05, 0.1],
                         [0.05, 0.1, 0.3]]
        
        # Output singletons
        # A[2,2] != 0.0 to compensate for platform offset!
        # Can eliminate static error at platform origin
        self.A = [[11.5, 10.75, 10.0, 9.25, 8.5], 
                  [6.5, 5.75, 5, 4.25, 3.5], 
                  [1.5, 0.75, 0.3, -0.75, -1.5], 
                  [-3.5, -4.25, -5, -5.75, -6.5], 
                  [-8.5, -9.25, -10.0, -10.75, -11.5]]
        
        # Proposition vectors
        self.mu_e_x = [0 for i in range(len(self.e_trimf))]
        self.mu_e_y = [0 for i in range(len(self.e_trimf))]
        self.mu_de_x = [0 for i in range(len(self.de_trimf))]
        self.mu_de_y = [0 for i in range(len(self.de_trimf))]
        self.antecedent_x = [[0 for j in range(len(self.A))] for i in range(len(self.A))]
        self.antecedent_y = [[0 for j in range(len(self.A))] for i in range(len(self.A))]
                  
        self.x = [self.cam.x, self.cam.x]
        self.x_ref = [self.x[0]]
        self.y = [self.cam.y, self.cam.y]
        self.y_ref = [self.y[0]]
        self.ref_idx = 0
        self.e_x = [0,0]
        self.e_y = [0,0]
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

        ### Control law ###
        
        ### Compute fuzzy propositions ###
        for i in range(len(self.mu_e_x)):
            self.mu_e_x[i] = self.proposition_trimf(self.e_x[0],
                                                    self.e_trimf[i])
            self.mu_e_y[i] = self.proposition_trimf(self.e_y[0],
                                                    self.e_trimf[i])

        for i in range(len(self.mu_de_x)):
            self.mu_de_x[i] = self.proposition_trimf(self.e_x[0]-self.e_x[1],
                                                     self.de_trimf[i])
            self.mu_de_y[i] = self.proposition_trimf(self.e_y[0]-self.e_y[1],
                                                     self.de_trimf[i])        
        ### Compute fuzzy relations ###
        ### AND method: poduct ###
        for i in range(len(self.antecedent_x)):
            for j in range(len(self.antecedent_x)):
                self.antecedent_x[i][j] = self.mu_de_x[i] * self.mu_e_x[j]

        for i in range(len(self.antecedent_y)):
            for j in range(len(self.antecedent_y)):
                self.antecedent_y[i][j] = self.mu_de_y[i] * self.mu_e_y[j]

        ### Perform fuzzy implicaton and output aggregation. ###
        ### Outputs are singletons, so MIN is equal to multiplicaton ###
        self.phi_1.insert(0,0), self.phi_1.pop()
        self.phi_2.insert(0,0), self.phi_2.pop()
        for i in range(len(self.A)):
            for j in range(len(self.A[i])):
                self.phi_1[0] += self.antecedent_x[i][j] * self.A[i][j]
                self.phi_2[0] += self.antecedent_y[i][j] * self.A[i][j]

        self.__motors.move(self.phi_1[0], self.phi_2[0])
        #print(self.phi_1[0], self.phi_2[0])

        # Log data
        if self.__log_on:
            self.logger.writerow([time.time(),self.x[0],self.y[0],
                                  self.x_ref[self.ref_idx], self.y_ref[self.ref_idx],
                                  self.phi_1[0], self.phi_2[0]])
    
    def proposition_trimf(self, x, trimf):
        """
        Compute fuzzy proposition for triangular membership function.
        """
        mu = 0.0
        (L,C,R) = trimf
        if (x >= L) and (x <= C):
            mu = (x - L) / (C - L)
        elif (x > C) and (x <= R):
            mu = -(x - R) / (R - C)
            
        return mu
    
    def set_ref(self, x_ref, y_ref):
        """
        Set the reference position of the ball.
        x_ref and y_ref should be lists of the same size
        """
        self.x_ref = x_ref
        self.y_ref = y_ref
        self.ref_idx = 0
    
    def run(self):
        """
        Run update every Td
        """
        while not self.stopped.wait(self.Td):
            self.update()
        
        self.__cleanup()
        
    def __cleanup(self):    
        self.cam.cleanup()
        self.__motors.cleanup()
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
