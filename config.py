import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description='配置解析器')

    parser.add_argument('--input_image', default='./pics/image_3.png', help='输入图片路径')
    parser.add_argument('--output_path', default='./pics/A.xml', help='输出文件路径')
    parser.add_argument('-k', type=int, default=20, help='二值化像素值的阈值')
    parser.add_argument('--down_sampling', type=int, default=1, help='下采样幅度')
    parser.add_argument('-L', type=int, default=60, help='路口模板匹配值的大小，根据下采样幅度，越小的图片所需模板大小越小')
    parser.add_argument('-M', type=int, default=30, help='路口坐标误差阈值，根据下采样幅度，越小的图片所需路口容差大小越小')
    parser.add_argument('--tolerance', type=float, default=1, help='模板匹配的容忍值，如果图片不规整，适当将其调小，取值[0,1]')

    args = parser.parse_args()
    return args
