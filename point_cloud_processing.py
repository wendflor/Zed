import numpy as np
import open3d as o3d

def visualize_point_cloud(point_cloud_path):
    pcd = o3d.io.read_point_cloud(point_cloud_path)
    print(pcd)
    print(np.asarray(pcd.points))
    lookat = np.ndarray([3,1],dtype = np.float64)   
    lookat = [0.0,0.0,1]
    up = np.ndarray([3,1],dtype = np.float64) 
    up=[1,0.0,0.0]
    front = np.ndarray([3,1],dtype = np.float64) 
    front=[0.0,1,0.0]
    #o3d.visualization.draw_geometries([pcd], lookat, up, front)
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(pcd)
    o3d.visualization.ViewControl.set_lookat(vis.get_view_control(), [0,0,0])
    o3d.visualization.ViewControl.set_zoom(vis.get_view_control(), 0.8)
    vis.run()

if __name__ == "__main__":
    point_cloud_path = "zed_pc_ultra_normal.pcd"
    visualize_point_cloud(point_cloud_path)