# config_utils.py
import configparser
from typing import Dict, Any
import logging


def parse_coordinates(value: str) -> list:
    """
    Parse a comma-separated string of coordinates into a list of floats.
    
    Args:
    value (str): A comma-separated string of numbers.

    Returns:
    List[float]: A list of floats parsed from the provided string.
    """
    return [float(x.strip()) for x in value.split(',')]

def load_configuration(config_path: str) -> Dict[str, Any]:
    """
    Load and parse configuration from an INI file specified by config_path.

    Args:
    config_path (str): The file path to the configuration file.

    Returns:
    Dict[str, Any]: A dictionary containing parsed configuration options organized
                    by section keys such as mesh_parameters, file_paths, etc.
    """

    config = configparser.ConfigParser()
    config.read(config_path)
    
    # Extract and parse mesh parameters
    mesh_params = {
        'length': config.getfloat('mesh_parameters', 'length'),
        'width': config.getfloat('mesh_parameters', 'width'),
        'height': config.getfloat('mesh_parameters', 'height'),
        'nodes_per_direction': [int(x) for x in config.get('mesh_parameters', 'nodes_per_direction').split(',')]
    }
    
    # File path configuration
    file_paths = {
        'output_file': config.get('file_paths', 'output_file')
    }

    # Parse node sets
    node_sets = {section: parse_coordinates(config.get('NodeSets', section))
                 for section in config.options('NodeSets')}

    logging.info(f"{len(node_sets)} node sets found: {', '.join(node_sets.keys())}")

    # Parse element sets
    element_sets = {section: parse_coordinates(config.get('ElementSets', section))
                    for section in config.options('ElementSets')}
    
    logging.info(f"{len(element_sets)} element sets found: {', '.join(element_sets.keys())}")

    # Optionally parse material properties if the section exists
    if config.has_section('MaterialProperties'):
        material_properties = {prop: config.getfloat('MaterialProperties', prop)
                               for prop in config.options('MaterialProperties')}
        logging.info(f"Material properties defined: {', '.join(material_properties.keys())}")
    else:
        material_properties = {}
        logging.info("No material properties defined.")

    return {
        'mesh_parameters': mesh_params,
        'file_paths': file_paths,
        'node_sets': node_sets,
        'element_sets': element_sets,
        'material_properties': material_properties
    }
