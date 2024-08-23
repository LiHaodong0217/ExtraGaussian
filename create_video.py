import cv2
import os
import argparse

# 设置命令行参数解析
parser = argparse.ArgumentParser(description="将图片序列转换为视频")
parser.add_argument('image_folder', type=str, help="输入图片文件夹路径")
parser.add_argument('output_video', type=str, help="输出视频文件名")
parser.add_argument('--duration', type=int, default=4, help="视频时长（秒），默认为4秒")
args = parser.parse_args()

# 获取图片文件夹路径和输出视频文件名
image_folder = args.image_folder
video_name = args.output_video
duration = args.duration

# 获取文件夹中的所有图片文件名，并按顺序排序
images = [img for img in os.listdir(image_folder) if img.endswith(".png") or img.endswith(".jpg")]
images.sort()

# 计算视频的帧率
fps = len(images) / duration  # 根据指定的时长计算帧率

# 读取第一张图片以获取视频帧的宽度和高度
first_image_path = os.path.join(image_folder, images[0])
frame = cv2.imread(first_image_path)
height, width, layers = frame.shape

# 定义视频编码器并创建 VideoWriter 对象
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 使用 'mp4v' 编码器生成 .mp4 文件
video = cv2.VideoWriter(video_name, fourcc, fps, (width, height))

# 将每张图片写入视频
for image in images:
    image_path = os.path.join(image_folder, image)
    frame = cv2.imread(image_path)
    video.write(frame)

# 释放 VideoWriter 对象
video.release()

print(f"视频已成功保存为 {video_name}")