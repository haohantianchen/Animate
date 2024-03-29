import os
from PIL import Image

# 将一个文件夹中的所有图片按指定帧率拼接成gif
# 设置文件夹路径和输出GIF文件名
folder_path = '/raid/cvg_data/lurenjie/animatediff-cli-prompt-travel/stylize/mp4_kemu3girl/2023-12-28T06-17-16_00/00_detectmap/controlnet_openpose'  # 替换为你的文件夹路径
output_gif = '/raid/cvg_data/lurenjie/animatediff-cli-prompt-travel/projects/girl_kemu3/gif/openpose.gif'  # 替换为你的输出GIF文件名

# 获取文件夹中所有的PNG文件，并按名称排序
png_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]
png_files.sort()

# 创建一个图像列表，按名称顺序加载PNG文件
images = []
for png_file in png_files:
    file_path = os.path.join(folder_path, png_file)
    img = Image.open(file_path)
    images.append(img)

# 设置帧率（FPS）和保存为GIF
fps = 10  # 替换为你想要的帧率
images[0].save(output_gif, save_all=True, append_images=images[1:], duration=1000 // fps, loop=0)
