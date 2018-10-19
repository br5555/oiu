"""
Camera calibration module.
"""

import cv2
import ConfigParser

class CameraCalibration:
    """
    Helper camera calibration class.
    """

    def __init__(self, cam_idx, config_file):
        """
        Initialize the class.
        """

        self.config_file = config_file

        # Coordinate transform parameters
        self.ax = 1
        self.bx = 0
        self.ay = 1
        self.by = 0
        
        self.cam_idx = cam_idx
        self._capture = cv2.VideoCapture(self.cam_idx)
        if not self._capture:
            raise Exception("Can't capture from Camera {0}!".format(cam_idx))

        (res, self._image) = self._capture.read()

        # Platform region
        self.im_width = self._image.shape[1]
        self.im_height = self._image.shape[0]
        self.im_center = (self.im_width/2,self.im_height/2)
        self.rect_org_px = (0,0)
        self.rect_width_px = self._image.shape[1]
        self.rect_height_px = self._image.shape[0]
        self.rect_end_px = (self.rect_org_px[0] + self.rect_width_px,
                         self.rect_org_px[1] + self.rect_height_px)

        self.rect_width = 0.29 # Dimension along x-axis, in [m]
        self.rect_height = 0.29 # Dimension along y-axis, in [m]

        # Active coordinates
        self.active_pt = (0,0)

        # Info text
        self.info_text = 'Please select the upper-left corner.'

        # Calibration state
        self.is_org_set = False
        self.is_end_set = False
        
    def calibrate(self):
        """
        Calibrate the camera.
        """
        
        cv2.namedWindow("Camera calibration", cv2.WINDOW_AUTOSIZE)
        # Get image coordinates of platform origin
        cv2.setMouseCallback("Camera calibration", self.set_org)
        while not self.is_org_set:
            (res, self._image) = self._capture.read()
            self.decorate_image()
            cv2.imshow("Camera calibration", self._image)
            cv2.waitKey(20)

        # Get image coordinates of platform end
        cv2.setMouseCallback("Camera calibration", self.set_end)
        self.info_text = "Please select the lower-right corner."
        while not self.is_end_set:
            (res, self._image) = self._capture.read()
            self.decorate_image()
            cv2.imshow("Camera calibration", self._image)
            cv2.waitKey(20)
            
        # Let the user test the calibration parameters
        cv2.setMouseCallback("Camera calibration", self.update_active_point)
        self.info_text = "Click to test. Press 'Esc' to quit."
        while True: 
            (res, self._image) = self._capture.read()
            self.decorate_image()
            cv2.imshow("Camera calibration",
                       self._image)
            if cv2.waitKey(20) & 0xFF == 27:
                break

        cv2.destroyAllWindows()
        self._capture.release()
        self.save()

    def set_org(self, event, x, y, flags, param):
        """
        On left mouse-click, store the rectangle origin coordinates.
        """
        if event == cv2.EVENT_LBUTTONUP:
            self.rect_org_px = (x,y)
            self.active_pt = (x,y)
            self.is_org_set = True

    def set_end(self, event, x, y, flags, param):
        """
        On left mouse-click, store the rectangle origin coordinates.
        """
        if event == cv2.EVENT_LBUTTONUP:
            self.rect_end_px = (x,y)
            self.active_pt = (x,y)
            self.compute_calibration()
            self.is_end_set = True

    def compute_calibration(self):
        self.ax = (self.rect_end_px[0] - self.rect_org_px[0])/self.rect_width
        self.bx = self.rect_org_px[0]
        self.ay = (self.rect_end_px[1] - self.rect_org_px[1])/self.rect_height
        self.by = self.rect_org_px[1]
        
    def update_active_point(self, event, x, y, flags, param):
        """
        On left mouse-click, prints the coordinates of the
        clicked point (expressed in the platform coordinate system)
        """
        if event == cv2.EVENT_LBUTTONUP:
            self.active_pt = (x,y)

    def decorate_image(self):

        # Print the info text
        (info_size, baseline) = cv2.getTextSize(self.info_text,
                                                cv2.FONT_HERSHEY_SIMPLEX,
                                                0.6, 1)
        cv2.putText(self._image, self.info_text,
                    (self.im_center[0] - info_size[0]/2,
                     self.im_center[1] + info_size[1]/2),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255))
        
        # Draw the control area rectangle
        cv2.rectangle(self._image, self.rect_org_px, self.rect_end_px, (0,0,255),2)

        # Draw the active point
        cv2.circle(self._image, self.active_pt, 3, (0,255,255), 2)
        cv2.putText(self._image, '{0}'.format(self.to_platform(self.active_pt)),
                    self.active_pt, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255))

    def to_platform(self, pt):
        """
        Transforms the given (x,y) point from image to platform coordinates."
        """

        return ((pt[0]-self.bx)/self.ax, (pt[1]-self.by)/self.ay)

    def save(self):
        config = ConfigParser.RawConfigParser()
        config.read(self.config_file)
        if not config.has_section('Camera'):
            config.add_section('Camera')
            config.set('Camera','cam_idx',str(0))

        config.set('Camera','ax',str(self.ax))
        config.set('Camera','bx',str(self.bx))
        config.set('Camera','ay',str(self.ay))
        config.set('Camera','by',str(self.by))
        config.set('Camera','rect_org_px',str(self.rect_org_px))
        config.set('Camera','rect_end_px',str(self.rect_end_px))

        with open(self.config_file, 'wb') as configfile:
            config.write(configfile)

        print('Configuration written to {0}!'.format(self.config_file))

if __name__ == '__main__':

    cam = CameraCalibration(0,'platform.cfg')
    cam.calibrate()
    
