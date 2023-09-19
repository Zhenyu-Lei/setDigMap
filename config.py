import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description='配置解析器')

    parser.add_argument('--input_image', default='./pics/map1.jpg', help='输入图片路径')
    parser.add_argument('--output_path', default='./pics/A.xml', help='输出文件路径')
    parser.add_argument('-k', type=int, default=20, help='像素值的阈值')
    parser.add_argument('--down_sampling', type=int, default=1, help='下采样幅度')
    parser.add_argument('-L', type=int, default=60, help='路口模板匹配值的大小')

    args = parser.parse_args()
    return args
