from typing import Tuple, List


def generate_3d_mesh(length: float, width: float, height: float, nodes_per_direction: list) -> tuple:
    # Example implementation for demonstration
    dx = length / (nodes_per_direction[0] - 1)
    dy = width / (nodes_per_direction[1] - 1)
    dz = height / (nodes_per_direction[2] - 1)

    nodes = []
    elements = []
    node_id = 1

    for i in range(nodes_per_direction[0]):
        for j in range(nodes_per_direction[1]):
            for k in range(nodes_per_direction[2]):
                nodes.append((node_id, i*dx, j*dy, k*dz))
                node_id += 1

    elem_id = 1
    for i in range(nodes_per_direction[0]-1):
        for j in range(nodes_per_direction[1]-1):
            for k in range(nodes_per_direction[2]-1):
                n1 = i * nodes_per_direction[1] * nodes_per_direction[2] + j * nodes_per_direction[2] + k + 1
                n2 = n1 + nodes_per_direction[2] * nodes_per_direction[1]
                n3 = n2 + nodes_per_direction[2]
                n4 = n1 + nodes_per_direction[2]
                n5 = n1 + 1
                n6 = n2 + 1
                n7 = n3 + 1
                n8 = n4 + 1
                elements.append((elem_id, n1, n2, n3, n4, n5, n6, n7, n8))
                elem_id += 1

    return nodes, elements

def define_node_set(nodes: List[Tuple[int, float, float, float]], box_min: List[float], box_max: List[float]) -> List[int]:
    """
    Identifies nodes within a specified bounding box.
    """
    box_nodes = []
    for node in nodes:
        node_id, x, y, z = node
        if box_min[0] <= x <= box_max[0] and box_min[1] <= y <= box_max[1] and box_min[2] <= z <= box_max[2]:
            box_nodes.append(node_id)
    return box_nodes

def define_element_set(elements: List[Tuple[int, ...]], nodes: List[Tuple[int, float, float, float]], box_min: List[float], box_max: List[float]) -> List[int]:
    """
    Defines an element set within a specified bounding box.
    """
    box_elements = []
    for elem in elements:
        if all(box_min[0] <= nodes[node_id-1][1] <= box_max[0] and
               box_min[1] <= nodes[node_id-1][2] <= box_max[1] and
               box_min[2] <= nodes[node_id-1][3] <= box_max[2] for node_id in elem[1:]):
            box_elements.append(elem[0])
    return box_elements
