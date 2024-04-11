# scanner/scanner.py
import os
import logging
from datetime import datetime
from .db import connect_db, delete_files_by_name, find_scanned_drives


def scan_hard_drive(scan_dir, hard_drive_name, db_name):
    logging.info(f'Adding drive: {hard_drive_name}, located at: {scan_dir}')
    
    conn, cursor = connect_db(db_name)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            format TEXT,
            hard_drive TEXT,
            date TEXT,
            path TEXT,
            size INTEGER,
            description TEXT
        )
    ''')
    
    for root, dirs, files in os.walk(scan_dir):
        for file in files:
            file_path = os.path.join(root, file)
            file_name, file_format = os.path.splitext(file)
            file_size = os.path.getsize(file_path) / 1000000
            file_modified = datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
            cursor.execute('''
                INSERT INTO files (name, format, hard_drive, date, path, size)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (file_name, file_format, hard_drive_name, file_modified, file_path, file_size))
    
    conn.commit()
    conn.close()
    
    logging.info('Scan complete, exiting.')

def handle_duplicates(db_name, drive_name):
    drives = find_scanned_drives(db_name)
    
    if drive_name in drives:
        delete_files_by_name(db_name, drive_name)
        
    return True  # If the drive is new, indicate to proceed with scanning
