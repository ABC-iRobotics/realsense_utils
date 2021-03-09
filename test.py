## @package realsense_utils
#  Realsense Test
#
#  This module can be used to test the Relasense camera and the capabilities of the RealsenseController class

import numpy as np
import logging
import cv2
from realsense_control import RealsenseController, LOG_LEVELS # The functions globally defined in realsense_control can also be imported for low level access

def show_image_stream(image_stream):
    cv2.namedWindow('Image stream', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('Image stream', image_stream)
    cv2.waitKey(1)

if __name__ == "__main__":

    # Initialize
    realsense = RealsenseController()

try:
    realsense.initialize()
    while True:
        rgb, depth = realsense.get_frames()
        show_image_stream(rgb)

except KeyboardInterrupt:
    pass
except Exception as e:
    logging.error('An error occurred during the main loop:')
    print(e)
    pass

finally:
    # Stop streaming
    if realsense.is_streaming():
        realsense._log_level = LOG_LEVELS.SILENT
        if realsense.get_frames():
            realsense.camera_pipeline.stop()