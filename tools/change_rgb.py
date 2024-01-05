from PIL import Image
import os

# 根据mask中pixel的rgb值改变对应rgb帧pixel的rgb值
def process_images(input_folder, output_folder, target_color=(66, 0, 82), threshold=30):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".png"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            # 打开图像
            image = Image.open(input_path)
            pixels = image.load()

            # 处理每个像素
            for y in range(image.height):
                for x in range(image.width):
                    # 获取像素颜色
                    current_color = pixels[x, y]

                    # 计算与目标颜色的距离
                    distance = sum((current_color[i] - target_color[i]) ** 2 for i in range(3)) ** 0.5

                    # 如果颜色接近目标颜色，则保持不变，否则变为黑色
                    if distance <= threshold:
                        pixels[x, y] = current_color
                    else:
                        pixels[x, y] = (0, 0, 0)

            # 保存处理后的图像
            image.save(output_path)

if __name__ == "__main__":
    input_folder = "/raid/cvg_data/lurenjie/animatediff-cli-prompt-travel/stylize/mp4_kemu3girl/00_controlnet_image/controlnet_canny"  # 替换为你的输入文件夹路径
    output_folder = "/raid/cvg_data/lurenjie/animatediff-cli-prompt-travel/tools/mask_im"  # 替换为你的输出文件夹路径

    process_images(input_folder, output_folder)
