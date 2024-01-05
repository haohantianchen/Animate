from PIL import Image
import os

# 根据mask图片中pixel的rgb值将mask中的对应部分涂黑
def process_frames(input_frames_folder, input_masks_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 获取视频帧文件夹中的所有文件
    frame_files = os.listdir(input_frames_folder)

    for frame_file in frame_files:
        if frame_file.endswith(".png"):
            frame_path = os.path.join(input_frames_folder, frame_file)
            mask_path = os.path.join(input_masks_folder, frame_file)
            output_path = os.path.join(output_folder, frame_file)

            # 打开视频帧和对应的mask图像
            frame_image = Image.open(frame_path)
            mask_image = Image.open(mask_path)

            # 获取像素数据
            frame_pixels = frame_image.load()
            mask_pixels = mask_image.load()

            # 处理每个像素
            for y in range(frame_image.height):
                for x in range(frame_image.width):
                    # 获取mask图像中的像素颜色
                    mask_color = mask_pixels[x, y]

                    # 如果mask图像中的像素为黑色，则将视频帧中对应像素变为黑色
                    if mask_color == (150, 5, 61):
                        frame_pixels[x, y] = (0, 0, 0)

            # 保存处理后的视频帧
            frame_image.save(output_path)

if __name__ == "__main__":
    input_frames_folder = "/raid/cvg_data/lurenjie/animatediff-cli-prompt-travel/stylize/mp4_kemu3girl/00_controlnet_image/controlnet_openpose"  # 替换为视频帧文件夹的路径
    input_masks_folder = "/raid/cvg_data/lurenjie/animatediff-cli-prompt-travel/stylize/mp4_kemu3girl/2024-01-03T22-45-17-sample-mistoonanime_v20/00_detectmap/controlnet_seg"  # 替换为对应mask文件夹的路径
    output_folder = "/raid/cvg_data/lurenjie/animatediff-cli-prompt-travel/tools/image_mask_2"  # 替换为输出文件夹路径

    process_frames(input_frames_folder, input_masks_folder, output_folder)
