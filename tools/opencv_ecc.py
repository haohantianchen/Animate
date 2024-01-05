import cv2
import numpy as np
import os

# 对一个文件夹中的所有png图像做ecc图像对准
def get_gradient(im):
    # Calculate the x and y gradients using Sobel operator
    grad_x = cv2.Sobel(im, cv2.CV_32F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(im, cv2.CV_32F, 0, 1, ksize=3)
    # Combine the two gradients
    grad = cv2.addWeighted(np.absolute(grad_x), 0.5, np.absolute(grad_y), 0.5, 0)
    return grad

def register_images(base_image, target_image):
    # 转换为灰度图像
    gray_base = cv2.cvtColor(base_image, cv2.COLOR_BGR2GRAY)
    gray_target = cv2.cvtColor(target_image, cv2.COLOR_BGR2GRAY)

    # 计算梯度
    grad_base = get_gradient(gray_base)
    grad_target = get_gradient(gray_target)

    # 设置图像配准的参数
    warp_mode = cv2.MOTION_EUCLIDEAN
    warp_matrix = np.eye(2, 3, dtype=np.float32)

    # 设定迭代停止条件
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 1000, 1e-5)

    # 进行图像配准，使用梯度作为输入
    cc, warp_matrix = cv2.findTransformECC(grad_base, grad_target, warp_matrix, warp_mode, criteria)

    # 使用配准矩阵对目标图像进行变换
    rows, cols = gray_base.shape
    aligned_image = cv2.warpAffine(target_image, warp_matrix, (cols, rows), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)

    return aligned_image

# 文件夹路径
folder_path = '/raid/cvg_data/lurenjie/animatediff-cli-prompt-travel/tools/image_mask_2'
save_path = '/raid/cvg_data/lurenjie/animatediff-cli-prompt-travel/tools/ecc_2'

# 基准帧文件名
base_frame_filename = '00000000.png'

# 读取基准帧
base_frame_path = os.path.join(folder_path, base_frame_filename)
base_frame = cv2.imread(base_frame_path)

# 遍历文件夹下的所有帧并进行配准
for filename in os.listdir(folder_path):
    if filename.endswith('.png') and filename != base_frame_filename:
        # 读取目标帧
        target_frame_path = os.path.join(folder_path, filename)
        target_frame = cv2.imread(target_frame_path)

        # 进行图像配准
        aligned_frame = register_images(base_frame, target_frame)

        # 保存配准后的帧
        output_path = os.path.join(save_path, 'aligned_' + filename)
        cv2.imwrite(output_path, aligned_frame)

print('图像配准完成。')
