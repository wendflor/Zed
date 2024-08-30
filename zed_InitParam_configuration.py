import pyzed.sl as sl

# Set configuration parameters here
# Overview of avialable InitParams: https://www.stereolabs.com/docs/api/python/classpyzed_1_1sl_1_1InitParameters.html
init_params = sl.InitParameters()
init_params.camera_resolution = sl.RESOLUTION.HD2K 
init_params.camera_fps = 0
init_params.depth_mode = sl.DEPTH_MODE.NEURAL
init_params.coordinate_units = sl.UNIT.MILLIMETER
init_params.enable_image_enhancement = True
init_params.depth_minimum_distance = 300
init_params.depth_maximum_distance = 600

# Save init_params in "init_params.conf.yml" file
# File must not exist! Otherwise saving process won't be executed for safety reasons
init_params.save("init_params.conf")