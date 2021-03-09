## @package realsense_utils
#  Realsense Control
#
#  This module can be used to control the Realsense camera including its initialization
#  and getting image data from the data streams

import pyrealsense2 as rs
import numpy as np
import logging

## 
#  @brief Get configuration of the sensors. It is necessary for enable streams.
#  @return configuration of the sensors

def get_config():
    '''
    Get configuration of the sensors. It is necessary for enable streams.

    returns: configuration of the sensors
    '''
    config = rs.config()
    return config


## 
#  @brief Get pipeline of the sensors. It is necessary for enable streams.
#  @return pipeline of the sensors

def get_pipeline():
    '''
    Get pipeline of the sensors. It is necessary for enable streams.

    returns: pipeline of the sensors
    '''
    pipeline = rs.pipeline()
    return pipeline


## 
#  @brief Enable streams (color, depth) in case of SR300
#  @param config is the config for SR300
#  @param rows is the rows for the resolution, 640 is default
#  @param cols is the cols for the resolution, 480 is default
#  @param framerate is the framerate, 30 is default

def enable_stream_realsense(config, rows = 640, cols = 480, framerate = 30):
    '''
    Enable streams (color, depth)

    params:
     - config: the config for SR300 (from get_config())
     - rows: the rows for the resolution, 640 is default
     - cols: the columns for the resolution, 480 is default
     - framerate: the framerate, 30 is default
    '''
    config.enable_stream(rs.stream.depth, rows, cols, rs.format.z16, framerate)
    config.enable_stream(rs.stream.color, rows, cols, rs.format.bgr8, framerate)


## 
#  @brief Get frames of the sensors
#  @param pipeline is the pipeline
#  @return frames of the sensors

def get_frames(pipeline):
    '''
    Get frames of the sensors

    params:
     - pipeline (from get_pipeline())
    
    returns: frames of the sensors
    '''
    frames = pipeline.wait_for_frames()
    return frames


## 
#  @brief Get depth frames
#  @param frames is the frames coming from the sensor
#  @return the depth frame

def get_depth_frames(frames):
    '''
    Get depth frames

    params:
     - frames: the frames coming from the sensor (from get_frames())
    
    returns: the depth frame
    '''
    depth_frame = frames.get_depth_frame()
    return depth_frame


## 
#  @brief Get color frames
#  @param frames is the frames coming from the sensor
#  @return the color frame

def get_color_frames(frames):
    '''
    Get color frames

    params:
     - frames: the frames coming from the sensor (from get_frames())

    returns: the color frame
    '''
    color_frame = frames.get_color_frame()
    return color_frame


## 
#  @brief Convert frames to nparrays for later usage
#  @param image frames is the image frames coming from the sensor
#  @return images in nparray

def convert_img_to_nparray(image_frames):
    '''
    Convert frames to nparrays for later usage

    params:
     - image_frames: the image frames coming from the sensor (get_depth_frames()/get_color_frames())

    returns: images in nparray

    '''
    img_to_nparray = np.asanyarray(image_frames.get_data())
    return img_to_nparray

class LogLevels():
    '''
    Class for representing log levels
    '''
    def __init__(self):
        self.ALL = 0
        self.SILENT = 1

LOG_LEVELS = LogLevels()


class RealsenseController():
    '''
    Class for convenient control of the RealSense camera
    '''

    def __init__(self):
        '''
        Constructor, store camera configuration and pipeline
        '''
        self.camera_config = get_config()
        self.camera_pipeline = get_pipeline()
        self._log_level = LOG_LEVELS.ALL

    def initialize(self, width=640, height=480, frame_rate=30, bag_file_path = '', real_time_playback = False, output_bag_file_path = ''):
        '''
        Initialize the camera streams, start pipeline

        If input bag_file_path is provided, the camera is initialized from the file and is set up for playback
        Input real_time_playback (bool) is only used if bag_file_path is set
        '''
        try:
            if not bag_file_path == '':
                # Bag file path provided, initialize a device from the configs stored in the file
                rs.config.enable_device_from_file(self.camera_config, bag_file_path)

            enable_stream_realsense(self.camera_config, width, height, frame_rate)

            if not output_bag_file_path == '':
                # Output file path has been provided, save data streams and camera config to a bag file
                if bag_file_path == '':
                    self.camera_config.enable_record_to_file(output_bag_file_path)
                else:
                    if not self._log_level == LOG_LEVELS.SILENT:
                        logging.error('Cannot do playback and save to file at the same time, no output will be saved')

            profile = self.camera_pipeline.start(self.camera_config)
            if not bag_file_path == '':
                # Set up playback       
                playback = profile.get_device().as_playback()
                playback.set_real_time(real_time_playback)
            return profile
        except Exception as e:
            if not self._log_level == LOG_LEVELS.SILENT:
                logging.error('Error during camera initialization, returning None')
                print(e)
            return None

    def get_frames(self):
        '''
        Get frames from camera as numpy arrays

        returns: (rgb, depth) tuple of numpy arrays containing the RGB and the depth images
        '''
        try:
            frames = get_frames(self.camera_pipeline)
            color_frame = get_color_frames(frames)
            depth_frame = get_depth_frames(frames)

            rgb = convert_img_to_nparray(color_frame)
            depth = convert_img_to_nparray(depth_frame)

            return (rgb, depth)
        
        except:
            if not self._log_level == LOG_LEVELS.SILENT:
                logging.error('Could not get frames from RealSense camera, returning None')
            return None

    def is_streaming(self):
        try:
            self.camera_pipeline.start(self.camera_config)
            self.camera_pipeline.stop()
            return False
        except Exception:
            return True

