from find_feature import process_image
from find_point import bfs
from config import parse_arguments
from edgeDetection import edge_detection

# 获取超参数
parser = parse_arguments()
# 获取路口信息
image_file = process_image(parser.input_image, down_sampling=parser.down_sampling, k=parser.k, L=parser.L)
# 获取点信息
bfs(image_file)
# 边缘检测
edge_detection(parser.input_image)
