from find_feature import process_image, process_image2, process_image3
from find_point import bfs, bfs2
from config import parse_arguments
from edgeDetection import edge_detection
from find_junction import find_nearest_points
from json_to_xml import convert_json_to_xml
from paint_result import paint_result
import time

# 获取超参数
parser = parse_arguments()

# 获取路口信息
start_time = time.time()
image_file = process_image2(parser.input_image, down_sampling=parser.down_sampling, k=parser.k, L=parser.L,
                            pix_thresholded=parser.tolerance)
end_time = time.time()
print("获取路口信息耗时：", end_time - start_time, "秒")

# 获取点信息
start_time = time.time()
points = bfs2(image_file, parser.input_image, down_sampling=parser.down_sampling)
end_time = time.time()
print("获取点信息耗时：", end_time - start_time, "秒")

# 边缘检测
start_time = time.time()
edge_detection(parser.input_image)
end_time = time.time()
print("边缘检测耗时：", end_time - start_time, "秒")

# 获取路口连接信息
start_time = time.time()
nearest_points = find_nearest_points(parser.input_image, points, threshold=parser.M, down_sampling=parser.down_sampling)
end_time = time.time()
print("获取路口连接信息耗时：", end_time - start_time, "秒")

# 保存xml文件
start_time = time.time()
convert_json_to_xml(nearest_points, parser.output_path, down_sampling=parser.down_sampling)
paint_result()
end_time = time.time()
print("保存xml文件耗时：", end_time - start_time, "秒")
