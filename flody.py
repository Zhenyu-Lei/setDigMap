import math


def build_adjacency_matrix(points, nearest_points, turn_penalty):
    n = len(points)
    matrix = [[math.inf] * n for _ in range(n)]  # 初始化邻接矩阵

    # 设置对角线上的元素为0
    for i in range(n):
        matrix[i][i] = 0

    # 根据nearest_points更新邻接矩阵中的边权重
    for edge in nearest_points:
        id1 = edge['id1']
        id2 = edge['id2']
        distance = edge['distance']

        # 计算转弯惩罚系数
        turn_penalty_factor = 1.0
        if id1 != id2:
            prev_id = id1 - 1 if id1 > 0 else n - 1
            if abs(points[prev_id].y - points[id1].y) >= 10 and abs(points[prev_id].x - points[id1].x) >= 10 and abs(
                    points[id1].y - points[id2].y) >= 10 or abs(points[id1].x - points[id2].x) >= 10:
                turn_penalty_factor = turn_penalty

        weighted_distance = distance * turn_penalty_factor
        matrix[id1][id2] = weighted_distance
        matrix[id2][id1] = weighted_distance  # 无向图，设置对称位置的权重相同
    return matrix


# 使用Floyd算法计算多源最短路径
def floyd_algorithm(adjacency_matrix):
    n = len(adjacency_matrix)

    # 初始化路径矩阵和距离矩阵
    path_matrix = [[None] * n for _ in range(n)]
    distance_matrix = adjacency_matrix

    # 更新路径矩阵和距离矩阵
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if distance_matrix[i][j] > distance_matrix[i][k] + distance_matrix[k][j]:
                    distance_matrix[i][j] = distance_matrix[i][k] + distance_matrix[k][j]
                    path_matrix[i][j] = k

    print(distance_matrix)
    print(path_matrix)
    return distance_matrix, path_matrix


def reconstruct_path(path_matrix, start, end):
    path = []
    now = end
    while now is not None:
        path.append(now)
        now = path_matrix[now][start]
    path.append(start)
    path=path[::-1]
    print(path)
    return path
