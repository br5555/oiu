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
        self.e_trimf = [ [-0.3 -0.1 -0.06667],
                         [-0.1 -0.06667 -0.03333],
                        [-0.06667 -0.03333 0],
                         [-0.03333 0 0.03333],
                         [0 0.03333 0.06667]
                         [0.0328 0.0661 0.0995]
                          [0.06667 0.1 0.3]]
        
        self.de_trimf = [ [-0.03 -0.01 -0.006667],
                         [-0.01 -0.006667 -0.003333],
                        [-0.00672 -0.00339 -5.29e-05],
                          [-0.003333 0 0.003333],
                          [-1.735e-18 0.003333 0.006667]
                           [0.003333 0.006667 0.01]
                           [0.006667 0.01 0.03]]
        
        # Output singletons
        # Rows: de
        # Columns: e
        self.A = [[   3.6618 *3.5,   3.3786 *3.5,   3.3078*3.5 ,   3.2370,    3.1662*0.02  ,  3.0954 *0.02  , 2.8122*0.02]
    [1.3959 *3.5 ,  1.1127*3.5   , 1.0419  ,  0.9711 ,   0.9003   , 0.8295*0.02  ,  0.5463*0.02]
    [0.9103  ,  0.6271  ,  0.5564  ,  0.4855   , 0.4147  ,  0.3439  ,  0.0608]
    [0.4248  ,  0.1416  ,  0.0708  ,       0  , -0.0708  , -0.1416,  , -0.4248]
   [-0.0608  , -0.3439  , -0.4147  , -0.4855  , -0.5564   ,-0.6271 ,  -0.9103]
   [-0.5463 *0.02 , -0.8295  *0.02, -0.9003  , -0.9711 ,  -1.0419  , -1.1127*0.02 ,  -1.3959*0.02]
   [-2.8122 *0.02 , -3.0954 *0.02 , -3.1662*0.02 ,  -3.2370  , -3.3078*0.02  , -3.3786 *0.02 , -3.6618*0.02]]
        
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


        self.phi_1[0] =0.8019 *self.phi_1[1] + self.phi_1[0]
        self.phi_2[0] =0.8019 *self.phi_2[1] + self.phi_2[0] 
        
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
