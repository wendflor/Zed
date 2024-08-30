import cv2
import pyzed.sl as sl
import numpy as np

def zed_image_capture_auto(init_params):
    # Create a ZED camera object
    zed = sl.Camera()

    # Open the camera
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        exit()

    # Get camera information (serial number)
    zed_serial = zed.get_camera_information().serial_number

    # Get calibration parameters due to recalibration during zed.open()
    CalibrationParameters= zed.get_camera_information().camera_configuration.calibration_parameters 
    #[LEFT_CAM_2K] 13.07.2024
    #fx=1904.98
    #fy=1905.72
    #cx=1093.33
    #cy=621.713
    #k1=-0.0671722
    #k2=-0.0293503
    #p1=-0.000199143
    #p2=0.000103017
    #k3=-0.0399208

    runtime_params = sl.RuntimeParameters()
    mat = sl.Mat() 
    
    err = zed.grab(runtime_params) 
    if err == sl.ERROR_CODE.SUCCESS: # Check that a new image is successfully acquired
        zed.retrieve_image(mat, sl.VIEW.LEFT) # Retrieve left image
        cvImage = mat.get_data() # Convert sl.Mat to cv2.Mat
        cv2.imwrite('calib_zed.png', cvImage)
        print('Image captured and saved as calib_zed.png')
    else:
        print("Error during capture : ", err)

    # Close the camera 
    zed.close()


if __name__ == "__main__":
    # Load init_params from configuration file
    init_params = sl.InitParameters()
    init_params.load("init_params.conf")
    zed_image_capture_auto(init_params)
    #zed_image_capture_manually(init_params)
    #zed_stereo(init_params)
