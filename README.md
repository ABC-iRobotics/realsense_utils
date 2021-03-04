# realsense_utils
Modules and info for Intel RealSense cameras


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

### Cameras and data_collection

Use the `data_collection_realsense.py` module to check if the program can work with the Realsense camera or not:
```bash
python data_collection_realsense.py
```
If the script is called without arguments it can be used to check if the data from the Realsense camera can be received.

The script can be used to record data for further processing, if it is called like:
```bash
python data_collection_realsense.py -record
```
In this case the data from the camera will be recorded in a new folder called `data` in a .bag file. It also saves the incoming data from the sensor fusion in a .txt file in the root of the repository. The name of the files can be set by the -filename argument.

Calling the script with the -playback option enables to check the contents of the previously recorded .bag files. The file can be selected with the -filename argument.

