import json
import math
from PIL import Image
import numpy as np
from flody import floyd_algorithm, build_adjacency_matrix, reconstruct_path


# 判断两个路口是否真的连接
def sample_image(img, coord1, coord2):
    # 将坐标转换为图像坐标
    x1, y1 = coord1
    x2, y2 = coord2
    img_coord1 = (int(x1), int(y1))
    img_coord2 = (int(x2), int(y2))

    # 在坐标之间取样 5 个点
    x_points = np.linspace(img_coord1[0], img_coord2[0], 5, dtype=int)
    y_points = np.linspace(img_coord1[1], img_coord2[1], 5, dtype=int)
    sample_points = [(x, y) for x, y in zip(x_points, y_points)]

    # 计算每个采样点的灰度值并求和
    grayscale_sum = sum([img.getpixel(p) for p in sample_points])

    return grayscale_sum


# 查找上方的连接路口
def find_nearest_up(img, x, y, points, threshold):
    closest = None
    min_distance = math.inf

    for point in points:
        if (x, y) == point:
            continue
        if abs(point.x - x) <= threshold and point.y < y and y - point.y < min_distance:
            closest = point
            min_distance = y - point.y

    # 判断是否为断头路
    if closest is not None:
        grayscale_sum = sample_image(img, (x, y), (closest.x, closest.y))
        if grayscale_sum < 1000:
            closest = None

    return closest


# 查找下方的连接路口
def find_nearest_down(img, x, y, points, threshold):
    closest = None
    min_distance = math.inf

    for point in points:
        if (x, y) == point:
            continue
        if abs(point.x - x) <= threshold and point.y > y and point.y - y < min_distance:
            closest = point
            min_distance = point.y - y

    # 判断是否为断头路
    if closest is not None:
        grayscale_sum = sample_image(img, (x, y), (closest.x, closest.y))
        if grayscale_sum < 1000:
            closest = None

    return closest


# 查找左边的连接路口
def find_nearest_left(img, x, y, points, threshold):
    closest = None
    min_distance = math.inf

    for point in points:
        if (x, y) == point:
            continue
        if abs(point.y - y) <= threshold and point.x < x and x - point.x < min_distance:
            closest = point
            min_distance = x - point.x

    # 判断是否为断头路
    if closest is not None:
        grayscale_sum = sample_image(img, (x, y), (closest.x, closest.y))
        if grayscale_sum < 1000:
            closest = None

    return closest


# 查找右边的连接路口
def find_nearest_right(img, x, y, points, threshold):
    closest = None
    min_distance = math.inf

    for point in points:
        if (x, y) == point:
            continue
        if abs(point.y - y) <= threshold and point.x > x and point.x - x < min_distance:
            closest = point
            min_distance = point.x - x

    # 判断是否为断头路
    if closest is not None:
        grayscale_sum = sample_image(img, (x, y), (closest.x, closest.y))
        if grayscale_sum < 1000:
            closest = None

    return closest


# 将找到的最近的相邻坐标点信息，附加到列表中
def append_nearest_point(nearest_points, point, closest_point):
    if closest_point is not None:
        max_diff = max(abs(point.x - closest_point.x), abs(point.y - closest_point.y))
        nearest_points.append({
            'id1': point.pid,
            'x1': point.x,
            'y1': point.y,
            'id2': closest_point.pid,
            'x2': closest_point.x,
            'y2': closest_point.y,
            'distance': max_diff,
        })


# 信息保存到junction_points.json
def save_closest_points(filename, closest_points):
    with open(filename, 'w') as f:
        json.dump(closest_points, f)

    print(f"Closest points saved to {filename}.")


# 查找给定坐标点列表中每个点的连接点
def find_nearest_points(input_image, points, threshold, down_sampling):
    # # 读取JSON文件
    # with open(file_path, 'r') as f:
    #     points = json.load(f)
    # 构建最近相邻坐标点列表
    nearest_points = []

    # Load the image and convert it to grayscale
    img = Image.open(input_image).convert('L')

    # 坐标还原
    for point in points:
        point.x = point.x * down_sampling
        point.y = point.y * down_sampling

    # 然后遍历文件中的坐标点，找到每个坐标点的最近相邻坐标点
    for point in points:
        pid = point.pid
        x = point.x
        y = point.y
        cls = point.cls

        if cls == 136 or cls == 160 or cls == 224 or cls == 152 or cls == 168 or cls == 248:
            closest_point = find_nearest_left(img, x, y, points, threshold)
            append_nearest_point(nearest_points, point, closest_point)

        if cls == 144 or cls == 136 or cls == 208 or cls == 152 or cls == 168 or cls == 248:
            closest_point = find_nearest_up(img, x, y, points, threshold)
            append_nearest_point(nearest_points, point, closest_point)

        if cls == 192 or cls == 224 or cls == 208 or cls == 152 or cls == 144 or cls == 248:
            closest_point = find_nearest_right(img, x, y, points, threshold)
            append_nearest_point(nearest_points, point, closest_point)

        if cls == 192 or cls == 160 or cls == 224 or cls == 208 or cls == 168 or cls == 248:
            closest_point = find_nearest_down(img, x, y, points, threshold)
            append_nearest_point(nearest_points, point, closest_point)

    # 将这些信息保存到'junction_points.json'
    _, path_matrix = floyd_algorithm(build_adjacency_matrix(points, nearest_points, 1))
    reconstruct_path(path_matrix, 1, 17)

    save_closest_points('./map_xml/junction_points.json', nearest_points)

    # 在这里跑多源最短Flody算法
    return nearest_points
