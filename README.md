# Realsense uils
Modules and info for Intel RealSense cameras

### Installation steps

Install pyrealsense2

 - With pip:
    ```bash
    pip install pyrealsense2
    ```

After the installation is complete, the pre-built packages of librealsense should be installed. For this follow the instructions [here](https://github.com/IntelRealSense/librealsense/blob/master/doc/distribution_linux.md), like this:

 - Register the keyserver's public key:
    ```bash
    sudo apt-key adv --keyserver keys.gnupg.net --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE || sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE
    ```

 - Add the server to the list of repositories:

    Ubuntu 16 LTS:
    ```bash
    sudo add-apt-repository "deb http://realsense-hw-public.s3.amazonaws.com/Debian/apt-repo xenial main" -u
    ```
    Ubuntu 18 LTS:
    ```bash
    sudo add-apt-repository "deb http://realsense-hw-public.s3.amazonaws.com/Debian/apt-repo bionic main" -u
    ```

 - Install the libraries:
 ```bash
 sudo apt-get install librealsense2-dkms
 sudo apt-get install librealsense2-utils
 ```

  - Optionally install the developer and debug packages:
  ```bash
  sudo apt-get install librealsense2-dev
  sudo apt-get install librealsense2-dbg
  ```

After these steps reboot your machine and disable secure boot in the system setup before booting Ubuntu again.

After the reboot (with secure boot disabled) run
```bash
realsense-viewer
```
in the command line. When the Realsense camera is connected to the machine its data should be available in Realsense-Viewer.


### Required python packages:
 - pyrealsense2
 - numpy
 - opencv-python (only for the test visualization, the Relasense utilities can be used without opencv)

### Using the camera with python

Import the `realsense_control` module to your python code to be able to use the utility functions for Realsense cameras:
```python
import realsense_control
```

Use  the provided RealsenseController class for ease of use:
```python
from realsense_control import RealsenseController

...

realsense = RealsenseController()
realsense.initialize()
rgb,depth = realsense.get_frames()
```

The other functions inside the `realsense_control` can also be imported and used for low-level access:

```python
import realsense_control

...

# Config camera and start streaming
config = realsense_control.get_config()
pipeline = realsense_control.get_pipeline()
realsense_control.enable_stream_realsense(config)
pipeline.start(config)

```

RealsenseController instances can be configured to use a real camera (default behavior):

```
realsense.initialize()
```

or to use a previously saved `bag` file to configure a virtual camera for playback:

```
realsense.initialize(bag_file_path='path/to/bag/file')
```

In order to save the stream to a bag file provide a path to the output bag file:
```
realsense.initialize(output_bag_file_path='path/to/output.bag')
```

While saving to a file, the `get_frames()` function can still be used.

The playback functionality and saving to a bag file **do not work at the same time**. If both are provided **only playback is performed**.

Use the parameters of the `initialize` function to set the resolution and framerate of the stream:
```
realsense.initialize(width=640, height=480, frame_rate=30)
```

**In playback mode the provided resolution and framerate should match with the resolution and framerate during the recording.**

### Test

The `test.py` script contains a simple example that shows how to use the `realsense_control` module. To run the test call:

```bash
python test.py
```

in the command line.

### Help

See the code documentation inside the `realsense_control.py` script for further info