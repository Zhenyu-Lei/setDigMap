import cv2
import numpy as np


def edge_detection(path):
    # 读取图像
    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    # 设定阈值，将小于阈值的像素设为0，大于阈值的像素设为128
    k = 20
    thresholded_image = np.where(image > k, 128, 0)

    height, width = thresholded_image.shape

    # 对处理过的图像进行边界检测
    edges = np.zeros((height, width))

    for dx, dy in [[0, 1], [1, 0], [0, -1], [-1, 0], [1, 1], [-1, 1], [1, -1], [-1, -1]]:
        diff = thresholded_image[1:height - 1, 1:width - 1] - thresholded_image[1 + dx:height - 1 + dx,
                                                              1 + dy:width - 1 + dy]
        edges[1:height - 1, 1:width - 1] += np.where(diff > 0, 255, 0)

    # 创建具有相同尺寸和通道数的新图像
    output_image = np.zeros_like(image)

    # 将边缘和阈值处理后的图像像素合并到新图像中
    output_image[thresholded_image == 128] = 128
    output_image[edges >= 255] = 255

    # 保存边缘图像
    cv2.imwrite('./pics/path_to_output_edges.png', edges)

    # 保存带有阈值处理后的图像像素信息的图像
    cv2.imwrite('./pics/path_to_output_image.png', output_image)


def edge_detection2(path):
    # 读取图像
    image = cv2.imread(path)  # rgb图，非黑白纯色

    # 设定阈值，将小于阈值的像素设为0，大于阈值的像素设为128
    k = 20
    thresholded_image = np.where(image > k, 128, 0)
    copy_image = thresholded_image.copy()  # 为方便自己对照着看原图和结果，使用副本找边界

    # 进行对角错位比较
    copy_image[1:, 1:, 0] = (thresholded_image[:-1, :-1, 1] != thresholded_image[1:, 1:,
                                                               2]) * 255  # 利用了rgb不同通道，以方便自己对照看结果

    # cc[:-1, :-1, 0] = (bb[:-1, :-1, 1] != bb[1:, 1:, 2]) * 255   # 用此句会使部分边界标到障碍上
    print(copy_image)
    cv2.imwrite('edge.png', copy_image)


if __name__ == '__main__':
    edge_detection('../pics/map2.jpg')
    # edge_detection2('../pics/map1.jpg')
