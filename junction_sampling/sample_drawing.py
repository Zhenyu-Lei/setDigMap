import json
from PIL import Image
import matplotlib.pyplot as plt
import random

# 读取json文件
with open('../map_xml/junction_points.json') as f:
    data = json.load(f)

# 获取数据中所有的起点id
start_ids = set(elem['id1'] for elem in data)
# 随机选择20个起点id
selected_start_ids = random.sample(start_ids, 20)

# 使用未经处理的原图像
img = Image.open('road_image.jpg')
# 绘制地图
fig, ax = plt.subplots()
ax.imshow(img)

# 绘制端点和连线
colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']
for start_id in selected_start_ids:
    # 提取当前起点id的匹配点
    matching_elements = [elem for elem in data if elem['id1'] == start_id]

    # 提取与起点匹配的每个终点的id和坐标
    end_ids = [elem['id2'] for elem in matching_elements]
    end_coords = [(elem['x2'], elem['y2']) for elem in matching_elements]

    # 绘制起点、终点以及连线
    ax.plot(int(matching_elements[0]['x1']), int(matching_elements[0]['y1']), 'r.')
    for i, (x2, y2) in enumerate(end_coords):
        ax.plot(x2, y2, 'g.', label=f'Endpoint {end_ids[i]}')
        ax.plot([int(matching_elements[0]['x1']), x2], [int(matching_elements[0]['y1']), y2], colors[2])

    ax.legend(['Starting Point', 'Endpoint'])

# 保存
plt.savefig('sample_draw.png', dpi=300)

# 展示
plt.show()
