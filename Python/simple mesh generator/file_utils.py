from typing import List, Tuple


def write_nodes_elements(filename: str, nodes: List[Tuple[int, float, float, float]], elements: List[Tuple[int, int, int, int, int, int, int, int, int]]) -> None:
    """
    Writes nodes and elements to a CalculiX input file.
    """
    with open(filename, 'w') as file:
        file.write('*Node\n')
        for node in nodes:
            file.write(f'{node[0]}, {node[1]}, {node[2]}, {node[3]}\n')

        file.write('*Element, type=C3D8\n')
        for elem in elements:
            file.write(f'{elem[0]}, {elem[1]}, {elem[2]}, {elem[3]}, {elem[4]}, {elem[5]}, {elem[6]}, {elem[7]}, {elem[8]}\n')

def write_set(filename: str, item_set: list, set_name: str, set_type: str) -> None:
    """
    Writes a node or element set to a CalculiX input file, formatting the output
    to list 16 numbers per line and removing the trailing comma on the last line.
    
    Parameters:
    - filename: the file to write to.
    - item_set: the list of items (nodes or elements) to write.
    - set_name: the name of the set.
    - set_type: 'node' for node sets, 'element' for element sets.
    """
    with open(filename, 'a') as file:
        # Different headers for node and element sets
        if set_type == 'node':
            file.write(f'*Nset, nset={set_name}\n')
        elif set_type == 'element':
            file.write(f'*Elset, elset={set_name}\n')
        
        # Writing up to 16 numbers per line
        total_items = len(item_set)
        for i in range(0, total_items, 16):
            slice_end = i + 16
            is_last_slice = slice_end >= total_items
            items_slice = item_set[i:slice_end]

            line = ', '.join(str(item_id) for item_id in items_slice)
            if not is_last_slice:
                line += ','
            
            file.write(f'{line}\n')


def write_surfaces(filename, element_sets, sides, names):
    """
    Writes multiple surfaces to the CalculiX input file.

    Parameters:
    filename (str): Path to the file.
    element_sets (list of str): List of element set names.
    sides (list of str): List of sides corresponding to each element set.
    names (list of str): List of names for each surface.
    """
    with open(filename, 'a') as file:
        file.write('** Surfaces ++++++++++++++++++++++++++++++++++++++++++++++++\n')
        for set_name, side, name in zip(element_sets, sides, names):
            file.write(f'*Surface, name={name}, type=ELEMENT\n')
            file.write(f'{set_name}, {side}\n')
        file.write('**\n**\n')
        
def write_material_properties(filename, material_name, property_names, values):
    """
    Writes material properties to the CalculiX input file.

    Parameters:
    filename (str): Path to the file.
    material_name (str): Name of the material.
    property_names (list of str): List of material property names.
    values (list): List of values for each property.
    """
    with open(filename, 'a') as file:
        file.write(f'** Materials ++++++++++++++++++++++++++++++++++++++++++++++++\n')
        file.write(f'**\n*Material, Name={material_name}\n')
        for prop_name, value in zip(property_names, values):
            file.write(f'*{prop_name}\n{value}\n')
        file.write('**\n')

def write_initial_conditions(filename, node_set, temperature):
    """
    Writes initial condtions to the CalculiX input file.
    """
    with open(filename, 'a') as file:
        file.write(f'** Initial Conditions ++++++++++++++++++++++++++++++++++++++++++++++++\n')
        file.write('**\n**\n')
        file.write('** Name: Initial_Temperature\n')
        file.write('*Initial conditions, Type=Temperature\n')
        file.write(f'{node_set}, {temperature}\n')
        file.write('**\n**\n')