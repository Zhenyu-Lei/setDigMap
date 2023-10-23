import json
from PIL import Image, ImageDraw, ImageFont


def paint_result():
    # 读取json文件
    with open('./map_xml/junction_points.json', 'r') as f:
        data = json.load(f)

    # 打开图像文件
    img = Image.open("./pics/boxs_image_bfs.png")

    # 创建绘图对象
    draw = ImageDraw.Draw(img)

    # 设置字体
    font = ImageFont.truetype('arial.ttf', 24)

    # 遍历json文件中的每个元素
    for item in data:
        # 获取起点坐标和终点坐标
        x1, y1 = item['x1'], item['y1']
        x2, y2 = item['x2'], item['y2']
        # 计算标注位置
        x, y = (x1 + x2) // 2, (y1 + y2) // 2
        # 获取距离值
        distance = item['distance']
        # 在图像上标注距离值
        draw.text((x, y), str(distance), font=font, fill='red')

    # 保存标注后的图像文件
    img.save('./pics/annotated_image.jpg')
