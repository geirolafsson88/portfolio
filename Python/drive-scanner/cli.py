# cli.py
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description='Drive Scanner and Database Search Tool')
    parser.add_argument('-n', '--new-scan', action='store_true', help='Initiate a new drive scan')
    parser.add_argument('-r', '--run-query', action='store_true', help='Execute an SQL query against the database')
    parser.add_argument('-l', '--list-drives', action='store_true', help='List hard drives already scanned')
    parser.add_argument('--del-drive', action='store_true',help='Delete data for a previously scanned drive')
    parser.add_argument('--db-path', action='store_true', help='Specify database path')
    parser.add_argument('--query', action='store_true', help='Specify SQL query to execute')
    parser.add_argument('--scan-dir', type=str, required=False, help='Directory to scan')
    parser.add_argument('--drive-name', type=str, required=False,  help='Name of the drive being scanned')

    return parser.parse_args()
