# main.py
import os
import logging
from config_loader import config
from utils import get_query_from_file, print_banner
from cli import parse_arguments
from scanner.scanner import scan_hard_drive, handle_duplicates
from scanner.db import execute_query, database_exists, list_scanned_drives, print_search, delete_files_by_name


logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

def main():
    print_banner()
    args = parse_arguments()
    
    # Check database path
    if args.db_path:
        args.db = input("Enter the path to the database: ")
    
    else:
        args.db = config['DEFAULT']['DatabasePath']
        logging.info(f'No database specified, using default: {args.db}')

    # Run the selected commands
    if args.new_scan:
        if not args.drive_name:
            args.drive_name = input("Enter the drive name to scan: ")
        
        if not args.scan_dir:
            args.scan_dir = input("Enter the path to scan (e.g., E:/): ")
        
        handle_duplicates(args.db, args.drive_name)
        scan_hard_drive(args.scan_dir, args.drive_name, args.db)
    
    elif args.run_query:
        if not database_exists(args.db):
            logging.info(f'Check database path, cannot find a database to read at the specified path {args.db}')
        
        if args.query:
            args.query = input("Enter the SQL query to run: ")
        
        else:
            query_file_path = os.path.join(os.path.dirname(__file__), 'config', config['DEFAULT']['DefaultQueryFile'])
            args.query = get_query_from_file(query_file_path)
            logging.info(f'Using query: {args.query}')
        
        search_results = execute_query(args.db, args.query)
        print_search(search_results)
    
    elif args.list_drives:
        print('\nAvailable drives:')
        list_scanned_drives(args.db)
    
    elif args.del_drive:
        list_scanned_drives(args.db)
        drive = input('\nEnter a drive to delete:')
        delete_files_by_name(args.db, drive)


if __name__ == "__main__":
    main()
