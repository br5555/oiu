"""
Image processing module for the 2DOF platform.
"""

import cv2
import ConfigParser
import csv
import time
from datetime import datetime

class CameraFeedback:
    """
    Image processing class. Provides ball localization.
    """

    def __init__(self, config_file, log = False):
        """
        Initialize image processing from config_file settings.
        """

        # Platform parameters
        config = ConfigParser.RawConfigParser()
        config.read(config_file)
        self.x = config.getfloat('Controller','x0')
        self.y = config.getfloat('Controller','y0')
        
        # Camera parameters
        self.cam_idx = config.getint('Camera','cam_idx')
        self.ax = config.getfloat('Camera','ax')
        self.bx = config.getfloat('Camera','bx')
        self.ay = config.getfloat('Camera','ay')
        self.by = config.getfloat('Camera','by')
        self.thresh = config.getint('Camera','thresh')
        org = config.get('Camera','rect_org_px')
        self.rect_org_px = tuple(int(i) for i in org.strip('()').split(','))
        end = config.get('Camera','rect_end_px')
        self.rect_end_px = tuple(int(i) for i in end.strip('()').split(','))
        self.ball_area_min = config.getint('Camera','ball_area_min')
        self.ball_area_max = config.getint('Camera','ball_area_max')
        self.x_px = self.rect_org_px[0] + int(self.rect_end_px[0] - self.rect_org_px[0])/2
        self.y_px = self.rect_org_px[1] + int(self.rect_end_px[1] - self.rect_org_px[1])/2

        # Algorithm parameters
        self.detected = False
        self.show_on = False
        self.debug_on = False
        self.__log_on = log

		# Data logging
        if self.__log_on:
            now_str = datetime.now().__str__().split('.')[0]
            now_str = now_str.replace(' ','-').replace(':','-')
            self.logfile = open(now_str + '_camera_log.csv','wb')
            self.logger = csv.writer(self.logfile, delimiter=';')
		
        self._capture = cv2.VideoCapture(self.cam_idx)
        if not self._capture:
            raise Exception("Can't capture from Camera {0}!".format(self.cam_idx))

        (success, self._image) = self._capture.read()
        self.decorated_image = self._image.copy() # Image for displaying
        self._image_gray = cv2.cvtColor(self._image, cv2.COLOR_RGB2GRAY)
        (ret, self._image_thresh) = cv2.threshold(self._image_gray, self.thresh,
                                          255, cv2.THRESH_BINARY)
        self.contours = []
        
    def update(self):
        """
        Update ball position reading from camera image.

        Returns ball position as (x,y) tuple.
        """

        self.detected = False
        ### Perform image segmentation to obtain contours ###
        (success, self._image) = self._capture.read()
        cv2.cvtColor(self._image, cv2.COLOR_RGB2GRAY, self._image_gray)
        cv2.threshold(self._image_gray, self.thresh, 255,
                      cv2.THRESH_BINARY, self._image_thresh)
        cv2.inRange(self._image_thresh, (240), (255), self._image_thresh)
        # Gaussian blurring removes small artefacts?
        cv2.GaussianBlur(self._image_thresh, (9,9), 0, self._image_thresh)
        [self.contours,hierarchy] = cv2.findContours(self._image_thresh[self.rect_org_px[1]:self.rect_end_px[1],
                                                                       self.rect_org_px[0]:self.rect_end_px[0]],
                                                    cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(self._image_thresh, self.contours, -1, (255,0,0), -1,
                         offset = self.rect_org_px)

        ### Process contours to find the right one (the ball on the plate) ###
        for cont in self.contours:
            m = cv2.moments(cont)
            area = m['m00']
            if (area > self.ball_area_min) and (area < self.ball_area_max):
                self.x_px = int(m['m10']/area) + self.rect_org_px[0]
                self.y_px = int(m['m01']/area) + self.rect_org_px[1]
                self.detected = True
                self.x = (self.x_px - self.bx) / self.ax
                self.y = (self.y_px - self.by) / self.ay
                break
            
        if self.__log_on:
            self.logger.writerow([time.time(),self.x,self.y])
		
        self.show_image()
        return (self.x, self.y)
        
    def run(self):
        """
        Calls the update method in a loop and prints
        estimated (x,y) coordinates.
        """
        while True:
            self.update()
            #print(self.x, self.y)
            if cv2.waitKey(1) & 0xFF == 27:
                break

        self.cleanup()
        
    def show_image(self):
        """
        Show original image.
        """
        
        # Always decorate the image, because somebody else might be showing it.
        self.decorate_image()
        if self.show_on:
            cv2.namedWindow('Camera image', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('Camera image', self.decorated_image)
        if self.debug_on:
            cv2.namedWindow('Grayscale image', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('Grayscale image', self._image_gray)
            cv2.namedWindow('Thresholded image', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('Thresholded image', self._image_thresh)
            
    def decorate_image(self):
        """
        Decorate original image with tracking area and ball estimate.
        """
        self.decorated_image = self._image.copy()
        cv2.rectangle(self.decorated_image, self.rect_org_px, self.rect_end_px, (0,0,255), 2)
        cv2.circle(self.decorated_image, (self.x_px,self.y_px), 10, (0,0,255), 2)
        
    def cleanup(self):
        self._capture.release()
        cv2.destroyAllWindows()
        if self.__log_on:
            self.logfile.close()
        
if __name__ == '__main__':

    cam = CameraFeedback('platform.cfg', log=True)
    cam.show_on = True
    cam.debug_on = True
    
    cam.run()
    
