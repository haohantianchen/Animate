import cv2
import os

# 将一个文件夹中的所有图片按指定帧率拼接成mp4
def images_to_video(input_folder, output_video, fps=24):
    image_files = sorted([f for f in os.listdir(input_folder) if f.endswith('.png')])

    if not image_files:
        print(f"No PNG images found in {input_folder}")
        return

    img = cv2.imread(os.path.join(input_folder, image_files[0]))
    height, width, layers = img.shape

    video = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    for image_file in image_files:
        img_path = os.path.join(input_folder, image_file)
        img = cv2.imread(img_path)
        video.write(img)

    cv2.destroyAllWindows()
    video.release()
    print(f"Video saved as {output_video}")

# 示例
input_folder = '/raid/cvg_data/lurenjie/animatediff-cli-prompt-travel/result/youtube/mp4_1_image'
output_video = '/raid/cvg_data/lurenjie/animatediff-cli-prompt-travel/result/youtube/mp4_1_768.mp4'
fps = 10

images_to_video(input_folder, output_video, fps)
