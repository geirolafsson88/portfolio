import os
import logging
from config_utils import load_configuration
from mesh_utils import generate_3d_mesh, define_node_set, define_element_set
from file_utils import write_nodes_elements, write_set

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main() -> None:
    # Determine the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Specify the configuration file name
    config_file = os.path.join(script_dir, 'config.ini')
    
    logging.info("Loading configuration from file: %s", config_file)
    config = load_configuration(config_file)
    
    logging.info("Generating 3D mesh.")
    nodes, elements = generate_3d_mesh(**config['mesh_parameters'])
    
    if nodes is None or elements is None:
        logging.error("Mesh generation failed.")
        return
    
    logging.info("Writing nodes and elements to file.")
    write_nodes_elements(config['file_paths']['output_file'], nodes, elements)
    
    logging.info("Writing nodesets to file.")
    for set_name, coords in config['node_sets'].items():
        node_set = define_node_set(nodes, coords[:3], coords[3:])
        write_set(config['file_paths']['output_file'], node_set, set_name, 'node')
        print(f"Processed Node Set: {set_name} with coordinates {coords}")

    logging.info("Writing element sets to file.")
    for set_name, coords in config['element_sets'].items():
        element_set = define_element_set(elements, nodes, coords[:3], coords[3:])
        write_set(config['file_paths']['output_file'], element_set, set_name, 'element')
        print(f"Processed Element Set: {set_name} with coordinates {coords}")
    
    logging.info("Writing material properites to file.")

    logging.info("Mesh generation and file operations completed successfully.")

if __name__ == '__main__':
    main()
