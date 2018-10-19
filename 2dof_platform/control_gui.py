"""
A simple GUI for interacting with platform controllers.
"""

import cv2

from math import pi, sin, cos

class ControlGui:
    """
    Provides a GUI for platform controllers.
    """
    def __init__(self, ctrl):
        self.ctrl = ctrl
        #self.info_text = "Press 'r' for rectangular or 'c' for circular reference."
        self.info_text = "Press 'c' for circular reference."
        self.im_width = self.ctrl.cam.decorated_image.shape[1]
        self.im_height = self.ctrl.cam.decorated_image.shape[0]
        
    def run(self):
        cv2.namedWindow("Platform control interface (press 'Esc' to quit)", cv2.WINDOW_AUTOSIZE)
        cv2.setMouseCallback("Platform control interface (press 'Esc' to quit)",
                             self.step_reference)
        while True:
            # Draw reference position
            x = self.ctrl.x_ref[self.ctrl.ref_idx]
            y = self.ctrl.y_ref[self.ctrl.ref_idx]
            x_px = int(self.ctrl.cam.ax * x + self.ctrl.cam.bx)
            y_px = int(self.ctrl.cam.ay * y + self.ctrl.cam.by)
            cv2.line(self.ctrl.cam.decorated_image,
                     (x_px-5,y_px),(x_px+5,y_px),(0,255,0),2)
            cv2.line(self.ctrl.cam.decorated_image,
                     (x_px,y_px-5),(x_px,y_px+5),(0,255,0),2)
            
            # Put info text
            #print(self.im_height, self.im_width)
            cv2.putText(self.ctrl.cam.decorated_image, self.info_text,
                        (50, self.im_height - 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,0))
                        
            cv2.imshow("Platform control interface (press 'Esc' to quit)", 
                       self.ctrl.cam.decorated_image)
            key = cv2.waitKey(120)
            if key & 0xFF == 27:
                break
            elif (key & 0xFF == 67) or (key & 0xFF == 99):
                self.circle_reference()
            #elif (key & 0xFF == 82) or (key & 0xFF == 114):
            #    self.rectangle_reference()
                
        cv2.destroyAllWindows()
    
    def step_reference(self, event, x, y, flags, param):
        """
        Update reference values on mouse/keyboard events.
        """
        if event == cv2.EVENT_LBUTTONUP:
            self.ctrl.set_ref([(x-self.ctrl.cam.bx)/self.ctrl.cam.ax],
                              [(y-self.ctrl.cam.by)/self.ctrl.cam.ay])
                              
    def rectangle_reference(self):
        """
        Set rectangle reference.
        """
        print('Pravokutnik!')
        
    def circle_reference(self):
        """
        Set circular reference.
        """
        T = 2*pi*5  # Period for a full circle, in seconds
        x0 = 0.14 # Circle center, x-coordinate
        y0 = 0.14 # Circle center, y-coordinate
        r = 0.1   # Radius
        x_ref = [x0 + r * sin(2*pi*k*self.ctrl.Td/T) for k in range(int(T/self.ctrl.Td))]
        y_ref = [y0 + r * cos(2*pi*k*self.ctrl.Td/T) for k in range(int(T/self.ctrl.Td))]
        
        self.ctrl.set_ref(x_ref, y_ref)
        
if __name__ == '__main__':
    pass