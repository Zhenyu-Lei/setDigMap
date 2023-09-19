import json
import xml.etree.ElementTree as ET
import xml.dom.minidom

def convert_json_to_xml(json_file_path, xml_file_path):
    # 读取json文件
    with open(json_file_path, 'r') as f:
        data = json.load(f)

    # 创建字典以存储点和连接
    points = {}
    connections = {}

    # 遍历json文件，将每个点按照id添加到字典中
    for element in data:
        id1 = element['id1']
        if id1 not in points:
            points[id1] = {
                'x': element['x1'],
                'y': element['y1']
            }

    # 遍历json文件，将每个连接添加到字典中
    for element in data:
        id1 = element['id1']
        id2 = element['id2']
        distance = element['distance']
        if id1 not in connections:
            connections[id1] = []
        connections[id1].append((id2, distance))

    # 创建xml文件
    root = ET.Element('osm', version='0.6')
    bounds = ET.SubElement(root, 'bounds', minlat='31.9250853363', minlon='117.125844043', maxlat='31.9464337951', maxlon='117.151790332')
    road = ET.SubElement(root, 'road', wayNum=str(len(points)))

    # 遍历各点并将其添加到xml文件中
    for id1, point in points.items():
        way = ET.SubElement(road, 'way', id=str(id1), pointNUM='1', type='')
        nd = ET.SubElement(way, 'nd', ref=str(id1), u=str(point['x']), v=str(point['y']), x=str(point['x']), y=str(point['y']))

    # 遍历所有连接，并按id1进行分组
    junction = ET.SubElement(root, 'junction', num=str(len(connections)))
    for id1, connections_list in connections.items():
        connect = ET.SubElement(junction, 'connect', id=str(id1))
        road1 = ET.SubElement(connect, 'road', id=str(id1), connectPoint=str(id1), distance=str('0'))
        for connection in connections_list:
            id2, distance = connection
            road2 = ET.SubElement(connect, 'road', id=str(id2), connectPoint=str(id2), distance=str(distance))

    # 解析为格式化字符串
    xml_str = ET.tostring(root, encoding='unicode', method='xml')
    dom = xml.dom.minidom.parseString(xml_str)
    formatted_xml = dom.toprettyxml(indent='    ')

    # 保存xml文件
    with open(xml_file_path, 'w') as f:
        f.write(formatted_xml)

convert_json_to_xml('junction_points.json', 'formatted_output.xml')
