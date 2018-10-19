"""
Motor control module for the 2DOF platform.

For details see, the Lynxmotion SSC-32 manual.
"""

import ConfigParser
import argparse
import serial
from math import pi

class Motors:
    """
    Sends control signals to the motors.
    """
    
    def __init__(self, config_file):
        """
        Connects to the motors.
        """
        
        ### Read config ###
        
        # Serial connection
        config = ConfigParser.RawConfigParser()
        config.read(config_file)
        self.port = config.get('Motors','port')
        self.baudrate = config.getint('Motors','baudrate')
        self.parity = config.get('Motors','parity')
        self.stopbits = config.getint('Motors','stopbits')
        self.bytesize = config.getint('Motors','bytesize')
        self.timeout = config.getint('Motors','timeout')
        self.write_timeout = config.getint('Motors','write_timeout')
        
        # Motor calibration parameters
        self.phi_1_max_pw = config.getfloat('Motors','phi_1_max_pw')
        self.phi_1_nul_pw = config.getfloat('Motors','phi_1_nul_pw')
        self.phi_1_min_pw = config.getfloat('Motors','phi_1_min_pw')
        self.phi_2_max_pw = config.getfloat('Motors','phi_2_max_pw')
        self.phi_2_nul_pw = config.getfloat('Motors','phi_2_nul_pw')
        self.phi_2_min_pw = config.getfloat('Motors','phi_2_min_pw')
        
        # Compute calibration coefficients
        # See the implementation of the move function
        # to figure out how these are used.
        self.b_phi_1 = self.phi_1_nul_pw
        self.a_phi_1_neg = -(self.phi_1_min_pw - self.b_phi_1) / (pi/2)
        self.a_phi_1_pos = (self.phi_1_max_pw - self.b_phi_1) / (pi/2)
        
        self.b_phi_2 = self.phi_2_nul_pw
        self.a_phi_2_neg = -(self.phi_2_min_pw - self.b_phi_2) / (pi/2)
        self.a_phi_2_pos = (self.phi_2_max_pw - self.b_phi_2) / (pi/2)
        
        ### Open the serial connection ###
        
        # Port seems to open automatically.
        self.__serial = serial.Serial(self.port, self.baudrate, 
                                      parity = self.parity,
                                      stopbits = self.stopbits, 
                                      bytesize = self.bytesize, 
                                      timeout = self.timeout,
                                      writeTimeout = self.write_timeout)
        
        if not self.__serial.isOpen():
            raise Exception("Can't connect to the motors!")
            
    def move_pw(self, phi_1, phi_2):
        """
        Move the servos to the desired setpoints,
        defined by pulse duration.
        
        Phi_1 and phi_2 are given as PWM impulse 
        duration values.
        """
        
        # Limit inputs
        if phi_1 < self.phi_1_min_pw:
            phi_1 = self.phi_1_min_pw
        elif phi_1 > self.phi_1_max_pw:
            phi_1 = self.phi_1_max_pw
            
        # Because the y-axis motor is mounted in the "reversed" direction,
        # the "min" pwm value (lowest point) is larger then the "max" pwm value (highest point)
        if phi_2 > self.phi_2_min_pw:
            phi_2 = self.phi_2_min_pw
        elif phi_2 < self.phi_2_max_pw:
            phi_2 = self.phi_2_max_pw
        
        self.__serial.write('#26 P{0} #8 P{1} \r'.format(phi_1, phi_2))
        
    def move(self, phi_1, phi_2):
        """ Move the servos to the desired setpoints,
            defined in radians.
        """
        
        # Convert desired setpoints from radians to impulses
        if phi_1 < 0:
            phi_1_pw = self.a_phi_1_neg * phi_1 + self.b_phi_1
        else:
            phi_1_pw = self.a_phi_1_pos * phi_1 + self.b_phi_1
            
        if phi_2 < 0:
            phi_2_pw = self.a_phi_2_neg * phi_2 + self.b_phi_2
        else:
            phi_2_pw = self.a_phi_2_pos * phi_2 + self.b_phi_2
        
        self.move_pw(phi_1_pw, phi_2_pw)
        
    def cleanup(self):
        self.__serial.close()
        
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Direct control of platform motors')
    parser.add_argument('phi_1', help = 'x-axis motor setpoint.', type = float)
    parser.add_argument('phi_2', help = 'y-axis motor', type = float)
    
    args = parser.parse_args()
    mot = Motors('platform.cfg')
    mot.move(args.phi_1, args.phi_2)
    mot.cleanup()
   
