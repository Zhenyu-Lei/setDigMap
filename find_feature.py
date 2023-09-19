import cv2
import numpy as np
import os
from find_point import find_junction,bfs


def process_image(image_path, down_sampling=4, k=20, L=15, pix_thresholded=1):
    if os.path.exists(f'processed_image_{down_sampling}_{k}_{L}_{pix_thresholded}.png'):
        print("processed_image.jpg has exist")
        return cv2.imread(f'processed_image_{down_sampling}_{k}_{L}_{pix_thresholded}.png', cv2.IMREAD_GRAYSCALE)
    else:
        # 1. 读取灰度图像
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        # 下采样参数
        scale_factor = 1 / down_sampling  # 缩小 8 倍

        # 计算新的图像尺寸
        new_width = int(image.shape[1] * scale_factor)
        new_height = int(image.shape[0] * scale_factor)
        new_size = (new_width, new_height)

        # 进行下采样
        resized_image = cv2.resize(image, new_size)

        # 2. 设定阈值超参数k并进行图像阈值处理
        thresholded_image = np.where(resized_image > k, 128, 0)
        # cv2.imwrite('thresholded_image.jpg', thresholded_image)

        # 3. 构建垂直方向的直角模板
        # vertical_templates = create_corner_templates(L)
        vertical_num = [64, 32, 16, 8]

        # 4. 添加边界padding
        thresholded_image = np.pad(thresholded_image, L, mode='constant', constant_values=0)

        # 4. 遍历整张图片，使用模板进行匹配，并进行灰度值按位"或"运算
        processed_image = np.copy(thresholded_image)  # 创建一个副本用于处理
        height, width = thresholded_image.shape

        # 复制一份相同的图片出来
        copy_image = np.copy(thresholded_image)

        # 由于图象可能会有像素级缺损，给定一个满足条件的阈值 pix_thresholded
        for y in range(height):
            if y % 100 == 0:
                print(y)
            for x in range(width):
                # 边界处理
                if x < L or x > width - L or y < L or y > height - L:
                    continue

                # 用矩形模板匹配，复杂度为n^2
                # for i, template in enumerate(vertical_templates):
                #     if (template[0] * copy_image[y:y + L, x:x + L]).sum() == 128 * (2 * L - 1):
                #         y_pad = template[1]
                #         x_pad = template[2]
                #         padded_image[y + y_pad, x + x_pad] = padded_image[y + y_pad, x + x_pad] | vertical_num[i]

                # 手动涉及4个匹配模板，复杂度n
                # (开口向↘)
                if (copy_image[y:y + L, x]).sum() >= 128 * L * pix_thresholded and (
                        copy_image[y, x:x + L]).sum() >= 128 * L * pix_thresholded:
                    thresholded_image[y, x] = thresholded_image[y, x] | vertical_num[0]
                # (开口向↙)
                if (copy_image[y:y + L, x]).sum() >= 128 * L * pix_thresholded and (
                        copy_image[y, x - L + 1:x + 1]).sum() >= 128 * L * pix_thresholded:
                    thresholded_image[y, x] = thresholded_image[y, x] | vertical_num[1]
                # (开口向↗)
                if (copy_image[y - L + 1:y + 1, x]).sum() >= 128 * L * pix_thresholded and (
                        copy_image[y, x:x + L]).sum() >= 128 * L * pix_thresholded:
                    thresholded_image[y, x] = thresholded_image[y, x] | vertical_num[2]
                # (开口向↖)
                if (copy_image[y - L + 1:y + 1, x]).sum() >= 128 * L * pix_thresholded and (
                        copy_image[y, x - L + 1:x + 1]).sum() >= 128 * L * pix_thresholded:
                    thresholded_image[y, x] = thresholded_image[y, x] | vertical_num[3]

        # 6. 删除边界padding
        processed_image = thresholded_image[L:-L, L:-L]

        # 7. 保存灰度图
        cv2.imwrite(f'./pics/processed_image_{down_sampling}_{k}_{L}_{pix_thresholded}.png', processed_image)

        # 8. 返回文件路径
        return processed_image


if __name__ == '__main__':
    image_file = process_image('./pics/map1.jpg', down_sampling=1, L=60)
    bfs(image_file)
