import cv2
import numpy as np
import matplotlib.pyplot as plt


# 计算每一行和每一列的灰度值总和
def peak_process_image(img, paint=False):
    gray_img = img

    # 计算每一列和每一行的灰度值之和
    sum_of_y = np.sum(gray_img, axis=1)
    sum_of_x = np.sum(gray_img, axis=0)

    if paint:
        # 将结果可视化并保存为.jpg文件
        plt.plot(sum_of_y)
        plt.savefig('./pics/sum_of_y.jpg')
        plt.clf()

        plt.plot(sum_of_x)
        plt.savefig('./pics/sum_of_x.jpg')

    # 返回x轴每个值所在列和y轴每个值所在行的灰度的和
    return sum_of_y, sum_of_x


# sum_of_y, sum_of_x = process_image('roadImage.jpg')


def find_peak_ranges(sum_of_y, sum_of_x):
    y_derivatives = [int(sum_of_y[i + 1]) - int(sum_of_y[i]) for i in range(len(sum_of_y) - 1)]
    x_derivatives = [int(sum_of_x[i + 1]) - int(sum_of_x[i]) for i in range(len(sum_of_x) - 1)]

    threshold = min(max(map(abs, y_derivatives)), max(map(abs, x_derivatives))) * 0.01
    y_peak_ranges = []
    x_peak_ranges = []

    start_index = None
    end_index = None
    for i in range(len(y_derivatives)):
        if y_derivatives[i] > threshold:
            if end_index is not None and start_index is not None:
                y_peak_ranges.append((start_index, end_index))
                start_index = None
                end_index = None
            if start_index is None:
                start_index = i
        if y_derivatives[i] < -threshold and start_index is not None:
            end_index = i
    if end_index is not None and start_index is not None:
        y_peak_ranges.append((start_index, end_index))

    start_index = None
    end_index = None
    for i in range(len(x_derivatives)):
        if x_derivatives[i] > threshold:
            if end_index is not None and start_index is not None:
                x_peak_ranges.append((start_index, end_index))
                start_index = None
                end_index = None
            if start_index is None:
                start_index = i
        elif x_derivatives[i] < -threshold and start_index is not None:
            end_index = i
    if end_index is not None and start_index is not None:
        x_peak_ranges.append((start_index, end_index))

    return y_peak_ranges, x_peak_ranges


# 将y轴方向和x轴方向每个峰值的起始值和结束值两两组合
def generate_peak_ranges(y_peak_ranges, x_peak_ranges):
    # 将y轴方向和x轴方向每个峰值的起始值和结束值两两组合，生成可以表示一个区域的[x1, y1, x2, y2]的新列表
    peak_range_list = [[x_peak_range[0], y_peak_range[0], x_peak_range[1], y_peak_range[1]]
                       for y_peak_range in y_peak_ranges for x_peak_range in x_peak_ranges]

    # 将结果转换为列表并按照起始值排序
    unique_peak_range_list = sorted(list(peak_range_list), key=lambda x: x[0])

    # 返回去重后的结果
    return unique_peak_range_list
