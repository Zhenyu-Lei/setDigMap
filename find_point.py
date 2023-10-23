from collections import deque

import numpy as np
import cv2
import json
from peakRange import peak_process_image, find_peak_ranges, generate_peak_ranges


class Point:
    def __init__(self, pid, y, x, cls):
        self.pid = pid
        self.y = y
        self.x = x
        self.cls = cls

    def __str__(self):
        return f"Point: pid={self.pid}, y={self.y}, x={self.x}, cls={self.cls}"


class Box:
    def __init__(self, y_min, x_min, y_max, x_max, score, cls):
        self.y_min = y_min
        self.x_min = x_min
        self.y_max = y_max
        self.x_max = x_max
        self.score = score
        self.cls = cls


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        return super().default(obj)


def to_json_and_save(points, file_path):
    point_dicts = [point.__dict__ for point in points]
    json_str = json.dumps(point_dicts, cls=NumpyEncoder)

    with open(file_path, "w") as file:
        file.write(json_str)


def reset_values(arr, value, new_value):
    mask = (arr == value)  # 创建一个布尔掩码，表示arr中值为value的位置
    arr[mask] = new_value  # 将掩码为True的位置的值置为new_value


def get_top_k_indices(arr, k):
    indices = np.argsort(arr)[-k:]  # 对数组进行升序排序，并取最后的k个索引
    return indices[::-1]  # 将索引顺序反转，得到前k个最大值的索引


def calculate_nonzero_lengths(arr, indices):
    selected_rows = arr[indices]  # 获取给定索引的行
    nonzero_values = np.where(selected_rows != 0)  # 获取非零值的索引位置
    arr = nonzero_values[1]
    current_sequence = 1
    longest_sequence = 1

    # 求最大的win_size
    for i in range(1, len(arr)):
        if arr[i] - arr[i - 1] == 1:
            current_sequence += 1
        else:
            longest_sequence = max(longest_sequence, current_sequence)
            current_sequence = 1

    longest_sequence = max(longest_sequence, current_sequence)
    return longest_sequence


def sliding_window(image, win_size, pixel_factor):
    height, width = image.shape
    boxes = []

    for y in range(height - win_size + 1):
        for x in range(width - win_size + 1):
            window = image[y:y + win_size, x:x + win_size]
            score = np.sum(window)

            if score != 0 and np.count_nonzero(window) / window.size >= pixel_factor:
                cls = np.argmax(np.bincount(window.flatten()[window.flatten() != 0]))
                boxes.append(Box(y, x, y + win_size - 1, x + win_size - 1, score, cls))

    return boxes


def non_max_suppression(boxes, overlap_threshold):
    boxes.sort(key=lambda box: box.score, reverse=True)

    selected_boxes = []
    while len(boxes) > 0:
        current_box = boxes[0]
        selected_boxes.append(current_box)
        boxes = boxes[1:]

        remaining_boxes = []
        for box in boxes:
            iou = calculate_iou(current_box, box)
            if iou < overlap_threshold:
                remaining_boxes.append(box)

        boxes = remaining_boxes

    return selected_boxes


def calculate_iou(box1, box2):
    intersection_y_min = max(box1.y_min, box2.y_min)
    intersection_x_min = max(box1.x_min, box2.x_min)
    intersection_y_max = min(box1.y_max, box2.y_max)
    intersection_x_max = min(box1.x_max, box2.x_max)

    intersection_area = max(0, intersection_y_max - intersection_y_min + 1) * max(0,
                                                                                  intersection_x_max - intersection_x_min + 1)

    area1 = (box1.y_max - box1.y_min + 1) * (box1.x_max - box1.x_min + 1)
    area2 = (box2.y_max - box2.y_min + 1) * (box2.x_max - box2.x_min + 1)

    union_area = area1 + area2 - intersection_area

    return intersection_area / union_area


def find_junction(process_image):
    copy_image = np.copy(process_image)
    # 1. 将二值图所有值为128的位置置为0
    reset_values(copy_image, 128, 0)

    # 2. 对每一行求和，找到top k的索引，在这些行上统计出搜索框的大小
    row_sums = np.sum(copy_image, axis=1)  # 对每一行进行求和
    top_indices = get_top_k_indices(row_sums, 5)
    # print(top_indices)

    # 3. 在给出的索引行上，统计非0连续值的最大和平均出现次数
    win_size = int(calculate_nonzero_lengths(copy_image, top_indices) * 1.3)

    # 4. 检索所有框，同时使用非极大值抑制的方式去除重框，然后返回points
    # 交并比的最大允许值
    overlap_threshold = 0.01
    # 要框住的像素值最小比率
    pixel_factor = 0.1
    print("find boxes")
    boxes = (sliding_window(copy_image, win_size, pixel_factor))
    print(f"all boxes {len(boxes)}")
    selected_boxes = non_max_suppression(boxes, overlap_threshold)

    # Convert selected_boxes to points
    selected_points = []
    for i, box in enumerate(selected_boxes):
        points_in_box = []
        for y in range(box.y_min, box.y_max + 1):
            for x in range(box.x_min, box.x_max + 1):
                if copy_image[y, x] == box.cls:
                    points_in_box.append((y, x))

        if points_in_box:
            avg_y = sum(point[0] for point in points_in_box) / len(points_in_box)
            avg_x = sum(point[1] for point in points_in_box) / len(points_in_box)
            selected_points.append(Point(i, int(avg_y), int(avg_x), box.cls))

    # Draw red pixels for selected points on the image
    for point in selected_points:
        process_image[point.y, point.x] = 0  # Set pixel color to red
        print(point)

    cv2.imwrite('./pics/boxs_image.png', process_image)
    to_json_and_save(selected_points, "./pics/point.json")
    return selected_points


def bfs(process_image, image_path, down_sampling):
    height, width = process_image.shape
    # 1. 将二值图所有值为128的位置置为0
    copy_image = np.copy(process_image)
    reset_values(copy_image, 128, 0)
    id_map = np.zeros((height, width), dtype=int)
    visited = np.zeros((height, width), dtype=bool)
    id_counter = 1
    points = []

    def get_neighbors(y, x):
        neighbors = []
        if y > 0:
            neighbors.append((y - 1, x))
        if y < height - 1:
            neighbors.append((y + 1, x))
        if x > 0:
            neighbors.append((y, x - 1))
        if x < width - 1:
            neighbors.append((y, x + 1))
        return neighbors

    def bfs_from_point(start_y, start_x):
        nonlocal id_counter
        queue = deque([(start_y, start_x)])
        visited[start_y, start_x] = True
        cls_counts = {}  # Count of each pixel value within the connected component
        while queue:
            y, x = queue.popleft()
            pixel_value = copy_image[y, x]
            id_map[y, x] = id_counter
            cls_counts[pixel_value] = cls_counts.get(pixel_value, 0) + 1

            for neighbor_y, neighbor_x in get_neighbors(y, x):
                if not visited[neighbor_y, neighbor_x] and copy_image[neighbor_y, neighbor_x] != 0:
                    visited[neighbor_y, neighbor_x] = True
                    queue.append((neighbor_y, neighbor_x))

        max_cls = max(cls_counts, key=lambda k: cls_counts[k])
        if cls_counts.get(248, 0) != 0:
            max_cls = 248
        y_mean = np.mean([point[0] for point in np.argwhere(id_map == id_counter)])
        x_mean = np.mean([point[1] for point in np.argwhere(id_map == id_counter)])
        points.append(Point(id_counter - 1, int(y_mean), int(x_mean), max_cls))
        id_counter += 1

    for y in range(height):
        for x in range(width):
            if not visited[y, x] and copy_image[y, x] != 0:
                bfs_from_point(y, x)

    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    # 下采样参数
    scale_factor = 1 / down_sampling  # 缩小 8 倍
    # 计算新的图像尺寸
    new_width = int(image.shape[1] * scale_factor)
    new_height = int(image.shape[0] * scale_factor)
    new_size = (new_width, new_height)

    # 进行下采样
    image = cv2.resize(image, new_size)

    # 将灰度图像转换为彩色图像
    process_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    # 绘制选定点的红色像素并标记 points.cls
    for point in points:
        x = point.x
        y = point.y
        cls = point.cls

        # 设置像素颜色为红色
        process_image[y, x] = (0, 0, 255)  # BGR颜色通道，红色为(0, 0, 255)

        # 在图像上标记 points.cls
        cv2.putText(process_image, str(point.pid) + '_' + str(cls), (x, y), cv2.FONT_HERSHEY_SIMPLEX, scale_factor,
                    (0, 255, 0), 1)  # 文本颜色为白色

    return points


def bfs2(process_image, image_path, down_sampling):
    height, width = process_image.shape
    # 重新计算peak，因为get_featrue是计算过padding的，坐标轴不一样
    sum_of_y, sum_of_x = peak_process_image(process_image)
    y_peak_ranges, x_peak_ranges = find_peak_ranges(sum_of_y, sum_of_x)
    peak_range_list = generate_peak_ranges(y_peak_ranges, x_peak_ranges)

    # 1. 将二值图所有值为128的位置置为0
    copy_image = np.copy(process_image)
    reset_values(copy_image, 128, 0)
    id_map = np.zeros((height, width), dtype=int)
    visited = np.zeros((height, width), dtype=bool)
    id_counter = 1
    points = []

    def get_neighbors(y, x):
        neighbors = []
        if y > 0:
            neighbors.append((y - 1, x))
        if y < height - 1:
            neighbors.append((y + 1, x))
        if x > 0:
            neighbors.append((y, x - 1))
        if x < width - 1:
            neighbors.append((y, x + 1))
        return neighbors

    def bfs_from_point(start_y, start_x):
        nonlocal id_counter
        queue = deque([(start_y, start_x)])
        visited[start_y, start_x] = True
        cls_counts = {}  # Count of each pixel value within the connected component
        while queue:
            y, x = queue.popleft()
            pixel_value = copy_image[y, x]
            id_map[y, x] = id_counter
            cls_counts[pixel_value] = cls_counts.get(pixel_value, 0) + 1

            for neighbor_y, neighbor_x in get_neighbors(y, x):
                if not visited[neighbor_y, neighbor_x] and copy_image[neighbor_y, neighbor_x] != 0:
                    visited[neighbor_y, neighbor_x] = True
                    queue.append((neighbor_y, neighbor_x))

        max_cls = max(cls_counts, key=lambda k: cls_counts[k])
        if cls_counts.get(248, 0) != 0:
            max_cls = 248
        y_mean = np.mean([point[0] for point in np.argwhere(id_map == id_counter)])
        x_mean = np.mean([point[1] for point in np.argwhere(id_map == id_counter)])
        points.append(Point(id_counter - 1, int(y_mean), int(x_mean), max_cls))
        id_counter += 1

    for peak_range in peak_range_list:
        for y in range(peak_range[1], peak_range[3] + 1):
            for x in range(peak_range[0], peak_range[2] + 1):
                if not visited[y, x] and copy_image[y, x] != 0:
                    bfs_from_point(y, x)

    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    # 下采样参数
    scale_factor = 1 / down_sampling  # 缩小 8 倍
    # 计算新的图像尺寸
    new_width = int(image.shape[1] * scale_factor)
    new_height = int(image.shape[0] * scale_factor)
    new_size = (new_width, new_height)

    # 进行下采样
    image = cv2.resize(image, new_size)

    # 将灰度图像转换为彩色图像
    process_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    # 绘制选定点的红色像素并标记 points.cls
    for point in points:
        x = point.x
        y = point.y
        cls = point.cls

        # 设置像素颜色为红色
        process_image[y, x] = (0, 0, 255)  # BGR颜色通道，红色为(0, 0, 255)

        # 在图像上标记 points.cls
        # cv2.putText(process_image, str(point.pid) + '_' + str(cls), (x, y), cv2.FONT_HERSHEY_SIMPLEX, scale_factor,
        #             (0, 255, 0), 1)  # 文本颜色为白色
        cv2.putText(process_image, str(point.pid), (x, y), cv2.FONT_HERSHEY_SIMPLEX, scale_factor,
                    (0, 255, 0), 1)  # 文本颜色为白色

    cv2.imwrite('./pics/boxs_image_bfs.png', process_image)
    to_json_and_save(points, "./pics/point.json")

    return points


if __name__ == '__main__':
    image = cv2.imread('processed_image_1_20_60_1.png', cv2.IMREAD_GRAYSCALE)
    # find_junction(image)
    bfs(image)
