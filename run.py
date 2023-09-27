from find_feature import process_image
from find_point import bfs
from config import parse_arguments
from edgeDetection import edge_detection
from find_junction import find_nearest_points
from json_to_xml import convert_json_to_xml

# 获取超参数
parser = parse_arguments()
# 获取路口信息
image_file = process_image(parser.input_image, down_sampling=parser.down_sampling, k=parser.k, L=parser.L,
                           pix_thresholded=parser.tolerance)
# 获取点信息
points = bfs(image_file, parser.input_image, down_sampling=parser.down_sampling)
# 边缘检测
edge_detection(parser.input_image)
# 获取路口连接信息
nearest_points = find_nearest_points(parser.input_image, points, threshold=parser.M, down_sampling=parser.down_sampling)
# 保存xml文件
convert_json_to_xml(nearest_points, parser.output_path, down_sampling=parser.down_sampling)
