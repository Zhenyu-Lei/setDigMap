import json
import xml.etree.ElementTree as ET
import xml.dom.minidom
import numpy as np

def convert_json_to_xml(nearest_points, output_path, down_sampling):
    # # 读取json文件
    # with open(json_file_path, 'r') as f:
    #     nearest_points = json.load(f)

    # 创建字典以存储点和连接
    # points = {}
    connections = {}

    # # 遍历json文件，将每个点按照id添加到字典中
    # for element in nearest_points:
    #     id1 = element['id1']
    #     if id1 not in points:
    #         points[id1] = {
    #             'x': element['x1'],
    #             'y': element['y1']
    #         }

    # 遍历json文件，将每个连接添加到字典中
    for i, element in enumerate(nearest_points):
        id1 = element['id1']
        id2 = element['id2']
        distance = element['distance']
        road_id = i + 1
        if id1 not in connections:
            connections[id1] = []
        connections[id1].append((road_id, id2, distance))

    # 创建xml文件
    root = ET.Element('osm', version='0.6')
    bounds = ET.SubElement(root, 'bounds', minlat='31.9250853363', minlon='117.125844043', maxlat='31.9464337951', maxlon='117.151790332')
    road = ET.SubElement(root, 'road', wayNum=str(len(nearest_points)))

    # 遍历各点并将其添加到xml文件中
    for i, path in enumerate(nearest_points):
        start_point = np.array([path["x1"], path["y1"]])
        end_point = np.array([path["x2"], path["y2"]])
        num_points = int(np.ceil(np.linalg.norm(end_point - start_point) * down_sampling / 50))
        points = np.linspace(start_point, end_point, num_points, endpoint=True)
        points = np.array(points)
        points = points.astype(int)

        way = ET.SubElement(root, 'way', road_id=str(i + 1), pointNUM=str(num_points + 1), type='')

        for j in range(num_points):
            nd = ET.SubElement(way, 'nd', ref=str(1000 * i + j + 1001), u=str(points[j][0]), v=str(points[j][1]),
                               x=str(points[j][0]), y=str(points[j][1]))

    # 遍历所有连接，并按id1进行分组
    junction = ET.SubElement(root, 'junction', num=str(len(connections)))
    for id1, connections_list in connections.items():
        connect = ET.SubElement(junction, 'connect', id=str(id1 + 1))
        for connection in enumerate(connections_list):
            road_id = connection[1][0]
            road2 = ET.SubElement(connect, 'road', road_id=str(road_id), connectPoint=str(1000 * road_id + 1))

    # 解析为格式化字符串
    xml_str = ET.tostring(root, encoding='unicode', method='xml')
    dom = xml.dom.minidom.parseString(xml_str)
    formatted_xml = dom.toprettyxml(indent='    ')


    # 保存xml文件
    with open(output_path, 'w') as f:
        f.write(formatted_xml)
    print(f"XML file saved to {output_path}.")

# convert_json_to_xml('./map_xml/junction_points.json', 'output.xml')




