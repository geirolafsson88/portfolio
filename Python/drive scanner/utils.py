import os


def print_banner():
    banner_path = os.path.join(os.path.dirname(__file__), 'config', 'banner.txt')
    try:
        with open(banner_path, 'r') as file:
            banner = file.read()
        print(banner)
    except Exception as e:
        print(f"Error reading banner file: {e}")

def get_query_from_file(query_file_path):
    """Reads an SQL query from a specified file and returns it as a string."""
    with open(query_file_path, 'r') as file:
        query = file.read()
    return query


