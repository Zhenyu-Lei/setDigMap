## setDigMap
该任务是对一张平面地图进行处理，完成拓扑结构的建立以及边缘检测

### 使用方法：

```shell
python run.py --down_sampling 2 -L 8 -k 20 --input_image './pics/map1.jpg' -M 10 --output_path './map_xml/formatted_output.xml'
```

>```python
>parser.add_argument('--input_image', default='./pics/map2.jpg', help='输入图片路径')
>parser.add_argument('--output_path', default='./pics/A.xml', help='输出文件路径')
>parser.add_argument('-k', type=int, default=20, help='二值化像素值的阈值')
>parser.add_argument('--down_sampling', type=int, default=4, help='下采样幅度')
>parser.add_argument('-L', type=int, default=15, help='路口模板匹配值的大小，根据下采样幅度，越小的图片所需模板大小越小')
>parser.add_argument('-M', type=int, default=30, help='路口坐标误差阈值，根据下采样幅度，越小的图片所需路口容差大小越小')
>parser.add_argument('--tolerance', type=float, default=1, help='模板匹配的容忍值，如果图片不规整，适当将其调小，取值[0,1]')
>```

### 拓扑结构的建立

1. 使用模板匹配的方式标注所有的**为路口的像素和其类型**，类型如下:

   <img src="pics/微信图片_20230914142006.png" style="zoom:50%;" />

2. 标注所有检测出路口的中心位置，Point的类型定义如下：

   ```python
   class Point:
       def __init__(self, pid, y, x, cls):
           self.pid = pid
           self.y = y
           self.x = x
           self.cls = cls
   
       def __str__(self):
           return f"Point: pid={self.pid}, y={self.y}, x={self.x}, cls={self.cls}"
   ```

3. 根据路口位置和类型，记录路口之间的连接关系。记录的信息如下：
   ```python
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
   ```
### 拓扑信息的保存
将连接关系转存成xml文件，方便下游规划任务。xml文件包含的信息如下：
   ```python
   # 道路信息
   way = ET.SubElement(root, 'way', road_id=str(i + 1), pointNUM=str(num_points + 1), type='')

   # 路口连接信息
   junction = ET.SubElement(root, 'junction', num=str(len(connections)))
   ```
