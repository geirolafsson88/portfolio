# scanner/db.py
import sqlite3
import os
import sys
import logging

# Check if a database already exists 
def database_exists(db_path):
    """Check if the database exists at the specified path."""
    return os.path.isfile(db_path)

# Connect to the database
def connect_db(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    return conn, cursor

# Query the database 
def execute_query(db_name, query, params=None):
    conn, cursor = connect_db(db_name)
    try:
        if params:
            cursor.execute(query, params)
    
        else:
            cursor.execute(query)
    
        # Add a commit here if the operation modifies the data
        if query.lower().startswith(("insert", "update", "delete")):
            conn.commit()
        
        return cursor.fetchall()
    
    except sqlite3.OperationalError as e:
        logging.error(f"An error occurred: {e}")
    
    finally:
        conn.close()

# Print query results to console
def print_search(results):
    """Prints the search results."""
    if not results:
        print('----------------------------------------------------------------------------')
        print('No matches found ):')
        print('----------------------------------------------------------------------------')
    
    for file in results:
        print('----------------------------------------------------------------------------')
        print(f"Name: {file[1]}")
        print(f"Format: {file[2]}")
        print(f"Hard Drive: {file[3]}")
        print(f"Modified Date: {file[4]}")
        print(f"Path: {file[5]}")
        print(f"File Size [mb]: {file[6]}")
        print(f"Description: {file[7]}")
        print('----------------------------------------------------------------------------')

# print the drives already in the database to console
# Modify the list_scanned_drives function
def list_scanned_drives(db_name):
    """Lists the names of all hard drives that have been scanned."""
    hard_drives = find_scanned_drives(db_name)

    if hard_drives:
        for index, drive_name in enumerate(hard_drives, start=1):
            print(f"{index}. {drive_name}")
    
    else:
        logging.error("No hard drives have been scanned.")
    
    return hard_drives  # Return the list after the loop

# discover what drives have alrady beeen scanned 
def find_scanned_drives(db_name):
    """Searches for unique hard drive names in database"""
    query = "SELECT DISTINCT hard_drive FROM files"
    results = execute_query(db_name, query)
    
    # unpack and return
    return [drive[0] for drive in results] if results else []

# make sure the user is sure
def confirm_overwrite(drive_name):
    confirm = input(f"Drive '{drive_name}' already scanned. Do you want to delete/overwrite its data? (y/n): ")
    
    if confirm.lower() == 'y':
        return True
    
    else:
        logging.info("Scan cancelled, exiting.")
        sys.exit(0)

# Delete file from database 
def delete_files_by_name(db_name, drive_name):
    if confirm_overwrite(drive_name):
        logging.info(f'Deleting data for drive: {drive_name}')
        query = 'DELETE FROM files WHERE hard_drive = ?'
        params = (drive_name,)
        execute_query(db_name, query, params)
