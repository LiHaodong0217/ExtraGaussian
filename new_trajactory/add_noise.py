# import numpy as np

# def add_noise_to_extrinsics_and_intrinsics(cam_extrinsics, cam_intrinsics, noise_std_extrinsics=0.008, noise_std_intrinsics=0.003):
#     noisy_extrinsics = {}
#     for img_id, extrinsic in cam_extrinsics.items():
#         # Add noise to both qvec (quaternion) and tvec (translation vector)
#         qvec_noise = np.random.normal(0, noise_std_extrinsics, extrinsic.qvec.shape)
#         tvec_noise = np.random.normal(0, noise_std_extrinsics, extrinsic.tvec.shape)
        
#         noisy_qvec = extrinsic.qvec + qvec_noise
#         noisy_tvec = extrinsic.tvec + tvec_noise
        
#         # Store the noisy extrinsics while keeping the same structure
#         noisy_extrinsics[img_id] = extrinsic._replace(qvec=noisy_qvec, tvec=noisy_tvec)
    
#     noisy_intrinsics = {}
#     for cam_id, intrinsic in cam_intrinsics.items():
#         # Add noise to the camera parameters (params attribute)
#         noise = np.random.normal(0, noise_std_intrinsics, intrinsic.params.shape)
#         noisy_params = intrinsic.params + noise
        
#         # Store the noisy intrinsics with the same structure
#         noisy_intrinsics[cam_id] = intrinsic._replace(params=noisy_params)
    
#     return noisy_extrinsics, noisy_intrinsics



# smooth deal
import numpy as np

def smooth_data(data, window_size=3):
    smoothed_data = np.convolve(data, np.ones(window_size)/window_size, mode='valid')
    return np.concatenate((data[:window_size-1], smoothed_data))

def add_noise_to_extrinsics_and_intrinsics(cam_extrinsics, cam_intrinsics, noise_std_extrinsics=0.008, noise_std_intrinsics=0.003):
    noisy_extrinsics = {}

    for img_id, extrinsic in cam_extrinsics.items():
        # Add noise to both qvec (quaternion) and tvec (translation vector)
        qvec_noise = np.random.normal(0, noise_std_extrinsics, extrinsic.qvec.shape)
        tvec_noise = np.random.normal(0, noise_std_extrinsics, extrinsic.tvec.shape)
        
        noisy_qvec = extrinsic.qvec + qvec_noise
        noisy_tvec = extrinsic.tvec + tvec_noise
        
        # Smooth the noisy tvec
        smoothed_tvec = smooth_data(noisy_tvec)
        
        # Store the noisy and smoothed extrinsics while keeping the same structure
        noisy_extrinsics[img_id] = extrinsic._replace(qvec=noisy_qvec, tvec=smoothed_tvec)
    
    noisy_intrinsics = {}
    for cam_id, intrinsic in cam_intrinsics.items():
        # Add noise to the camera parameters (params attribute)
        noise = np.random.normal(0, noise_std_intrinsics, intrinsic.params.shape)
        noisy_params = intrinsic.params + noise
        
        # Store the noisy intrinsics with the same structure
        noisy_intrinsics[cam_id] = intrinsic._replace(params=noisy_params)
    
    return noisy_extrinsics, noisy_intrinsics

