"""
Direct joystick control of the platform.
"""

import pygame
from motor_control_ssc32 import Motors

from math import pi

if __name__ == '__main__':
    
    pygame.init()
    pygame.joystick.init()
    motors = Motors('platform.cfg')
    
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    
    screen = pygame.display.set_mode((227, 250))
    c = pygame.time.Clock()
    img = pygame.image.load('attack3.jpg')
    
    done = False
    
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        
        ax1 = joystick.get_axis(0)
        ax2 = joystick.get_axis(1)
        
        screen.blit(img,(0,0))
        pygame.display.flip()
        motors.move(ax1*pi/2, ax2*pi/2)
        
    motors.cleanup()
    pygame.quit()
    