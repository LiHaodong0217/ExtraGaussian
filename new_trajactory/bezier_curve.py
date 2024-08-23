import numpy as np
from scipy.spatial.transform import Rotation as R
from scipy.interpolate import CubicSpline

# 贝塞尔曲线生成函数
def bezier_curve(points, n_points=100):
    n = len(points) - 1
    t = np.linspace(0, 1, n_points)
    curve = np.zeros((n_points, 3))
    
    for i in range(n_points):
        curve[i, :] = sum(
            binomial_coeff(n, k) * (1 - t[i])**(n-k) * t[i]**k * points[k]
            for k in range(n+1)
        )
    return curve

def binomial_coeff(n, k):
    from math import factorial
    return factorial(n) // (factorial(k) * factorial(n - k))

# 三次样条插值旋转四元数
def slerp_cubic(rotations, t_vals):
    cs = CubicSpline(t_vals, rotations, axis=0)
    interpolated_rotations = cs(t_vals)
    interpolated_rotations /= np.linalg.norm(interpolated_rotations, axis=1)[:, np.newaxis]
    return interpolated_rotations

# 生成变换矩阵
def create_transformation_matrices(sampled_points, sampled_rotations):
    n = sampled_points.shape[0]
    transformation_matrices = np.zeros((n, 4, 4))
    
    for i in range(n):
        rotation_matrix = R.from_quat(sampled_rotations[i]).as_matrix()
        transformation_matrices[i, :3, :3] = rotation_matrix
        transformation_matrices[i, :3, 3] = sampled_points[i]
        transformation_matrices[i, 3, 3] = 1.0
        
    return transformation_matrices

# 应用贝塞尔曲线生成新的相机位姿
def generate_new_camera_poses(cam_extrinsics):
    # 提取平移和旋转部分
    points = np.array([extrinsic.tvec for extrinsic in cam_extrinsics.values()])
    rotations = np.array([extrinsic.qvec for extrinsic in cam_extrinsics.values()])
    
    # 生成贝塞尔曲线
    curve = bezier_curve(points, n_points=100)
    
    # 均匀采样点和旋转四元数
    t_vals = np.linspace(0, 1, len(rotations))
    sampled_rotations = slerp_cubic(rotations, t_vals)
    
    # 生成新的相机外参矩阵
    transformation_matrices = create_transformation_matrices(curve, sampled_rotations)
    
    return transformation_matrices
