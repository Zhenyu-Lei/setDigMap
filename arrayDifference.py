import cv2
import numpy as np
import matplotlib.pyplot as plt


# 计算出每个点第0列到当前列的灰度和，以及第0行到当前行的灰度和
def calculate_gray_sum(img):

    height, width = img.shape

    # Initialize the result arrays
    sum_of_y = np.zeros((height, width))
    sum_of_x = np.zeros((height, width))

    # Calculate the cumulative sum of gray values within the specified range for each pixel
    for i in range(height):
        if i == 0:
            sum_of_y[i, :] = img[i, :]
        else:
            sum_of_y[i, :] = sum_of_y[i-1, :] + img[i, :]

    for j in range(width):
        if j == 0:
            sum_of_x[:, j] = img[:, j]
        else:
            sum_of_x[:, j] = sum_of_x[:, j-1] + img[:, j]

    # 返回结果
    return sum_of_y, sum_of_x
