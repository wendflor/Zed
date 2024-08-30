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
    # Configure displayed OpenCV Window 
    win_name = "left camera wiew"
    cv2.namedWindow(win_name)
    
    err = zed.grab(runtime_params) 
    if err == sl.ERROR_CODE.SUCCESS: # Check that a new image is successfully acquired
        zed.retrieve_image(mat, sl.VIEW.LEFT) # Retrieve left image
        cvImage = mat.get_data() # Convert sl.Mat to cv2.Mat
        cv2.imwrite('5r_5b_01.png', cvImage)
        cv2.imshow(win_name, cvImage) # Display image
        print('Image captured and saved as 5r_5b_01.png')
    else:
        print("Error during capture : ", err)

    # Close the camera 
    zed.close()

def zed_image_capture_manually(init_params):
    # Create a ZED camera object
    zed = sl.Camera()

    # Open the camera
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        exit()

    # Get camera information (serial number)
    # zed_serial = zed.get_camera_information().serial_number

    #calibration parameters change due to recalibration/rectification during zed.open()
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
    win_name = "left camera wiew"
    cv2.namedWindow(win_name)
    
    key = '0'
    while key != 113:  # for 'q' key
        err = zed.grab(runtime_params) 
        if err == sl.ERROR_CODE.SUCCESS: # Check that a new image is successfully acquired
            zed.retrieve_image(mat, sl.VIEW.LEFT) # Retrieve left image
            cvImage = mat.get_data() # Convert sl.Mat to cv2.Mat
            cv2.imshow(win_name, cvImage) #Display image
            if key == 115: # press 's' to save image 
                cv2.imwrite('manually_captured_image.png', cvImage)
        else:
            print("Error during capture : ", err)
            break

        key = cv2.waitKey(5)   

    # Close the camera 
    zed.close()

def zed_stereo(init_params):
    
    # Create a ZED camera object
    zed = sl.Camera()

    # Open the camera
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        exit()

    #fx = zed.get_camera_information().camera_configuration.calibration_parameters.left_cam.fx
    #fy = zed.get_camera_information().camera_configuration.calibration_parameters.left_cam.fy
    #cx = zed.get_camera_information().camera_configuration.calibration_parameters.left_cam.cx
    #cy = zed.get_camera_information().camera_configuration.calibration_parameters.left_cam.cy

    # dist_vec = zed.get_camera_information().camera_configuration.calibration_parameters.left_cam.disto
    # print(fx, fy, cx ,cy, dist_vec)
    # If auto calibration/ rectification (during zed.open) is already performed, all distortion values should be zero
        
    # Create a sl.Mat with float type (32-bit) 
    depth_zed = sl.Mat(zed.get_camera_information().camera_configuration.resolution.width, zed.get_camera_information().camera_configuration.resolution.height, sl.MAT_TYPE.F32_C1)
    point_cloud_zed = sl.Mat(zed.get_camera_information().camera_configuration.resolution.width, zed.get_camera_information().camera_configuration.resolution.height, sl.MAT_TYPE.F32_C1)
    if zed.grab() == sl.ERROR_CODE.SUCCESS:
        # Retrieve depth data (32-bit)
        zed.retrieve_measure(depth_zed, sl.MEASURE.DEPTH)
        # Load depth data into a numpy array
        depth_ocv = depth_zed.get_data()
        # Retrieve point cloud data
        zed.retrieve_measure(point_cloud_zed, sl.MEASURE.XYZRGBA)
        # point_cloud_zed.write("point_cloud_zed.ply")
        point_cloud_zed.write("zed_pc_neuralplus_normal.pcd")
        # Print the depth value at the center of the image
        #depth_dim = np.shape(depth_ocv)
        #print(depth_ocv[int(depth_dim[0]/2)][int(depth_dim[1]/2)])
        #print(depth_ocv)
        
    # Displaying Depth
    # 32-bit float np array can't be displayed with opencv. Normalizing depth values to 8-bit black and white representaion
    image_depth_zed = sl.Mat(zed.get_camera_information().camera_configuration.resolution.width, zed.get_camera_information().camera_configuration.resolution.height, sl.MAT_TYPE.U8_C4)
    if zed.grab() == sl.ERROR_CODE.SUCCESS:
        # Retrieve the normalized depth image
        zed.retrieve_image(image_depth_zed, sl.VIEW.DEPTH)
        # Use get_data() to get the numpy array
        image_depth_ocv = image_depth_zed.get_data()
        # Display the depth view from the numpy array
        cv2.imshow("Image", image_depth_ocv)
        cv2.waitKey(0) # Close window by pressing any button
    
    # Close the camera 
    zed.close()

    # Save depth values as .csv file
    # np.savetxt("Depth.csv", depth_ocv, delimiter=",")

    return depth_zed, point_cloud_zed


if __name__ == "__main__":
    # Load init_params from configuration file
    init_params = sl.InitParameters()
    init_params.load("init_params.conf")
    zed_image_capture_auto(init_params)
    #zed_image_capture_manually(init_params)
    #zed_stereo(init_params)
