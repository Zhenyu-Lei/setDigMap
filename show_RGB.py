import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import cv2


def show_figure(image_path):
    # 定义颜色映射
    color_map_values = [0, 128, 136, 144, 152, 160, 168, 192, 208, 224, 248]
    color_map_colors = ['#000000', '#FFFFFF', '#FF0000', '#00FF00', '#0000FF', '#FFFF00',
                        '#FF00FF', '#00FFFF', '#FF8000', '#8000FF', '#0080FF']
    cmap = ListedColormap(color_map_colors)

    # 创建示例二值图
    binary_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # 创建RGB图像
    rgb_image = np.zeros((binary_image.shape[0], binary_image.shape[1], 3), dtype=np.uint8)
    for i, value in enumerate(color_map_values):
        mask = binary_image == value
        rgb_color = np.array(tuple(int(color[i:i + 2], 16) for color in color_map_colors[i][1:]) + [255],
                             dtype=np.uint8)  # 将颜色字符串转换为RGB整数
        rgb_image[mask] = rgb_color

    # 绘制图像
    plt.imshow(rgb_image, cmap=cmap, interpolation='nearest')
    plt.axis('off')

    # 绘制图例
    legend_labels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
    legend_elements = [plt.Line2D([0], [0], marker='o', color='w', label=label,
                                  markerfacecolor=color, markersize=8) for label, color in
                       zip(legend_labels, color_map_colors)]
    plt.legend(handles=legend_elements, loc='lower right')

    # 显示图像
    plt.show()
