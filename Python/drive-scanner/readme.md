# Hard Drive Scanner
## Motivation
This piece of software performs a relatively simple task to solve a problem I faced. I was acquiring lots of data for multiple projects, the magnitude of data was into the tens of terrabytes. At least in the short term, I needed this data to be stored on local drives so that I could work remotely without adding unacceptable latency. The result was data scattered across multiple (identical in appearance) external hard drives. Whenever I was looking for something I had to plug each drive in one after another and hunt about what what I needed. 

And so Hard Drive Scanner was born. Hard Drive Scanner is a Python command-line tool designed to help users efficiently search through data stored on hard drives which are not currently connected to the computer. To achieve this, the code scans specified directories (or entire drives), extracting metadata about each file, and adding a hard drive tag which is all stored in a portable SQLite database. This SQLite database is suitable for cloud computing such as MS onedrive, where the file will always be backed up and synced to all your workspaces. 

The software also provides features to search the database using SQL queries providing powerful and highly customisable search functionality. The result of a search will be the corrosponding files, file location, and hard drive tag allowing the user to efficiently find the data they are looking for. 

## Features

- **Scan Mode**: Recursively scan a specified directory or drive, storing details about each file, including name, format, size, and last modified date.
- **Query Mode**: Execute SQL queries against the collected data to find files matching specific criteria.
- **List Mode**: List all drives that have been scanned and stored in the database.
- **Delete Mode**: Remove records of a previously scanned drive from the database, optionally after confirming with the user.

## Setup

To set up the Hard Drive Scanner, you will need Python 3.6 or higher. No external dependencies are required beyond the Python Standard Library.

1. Clone this repository to your local machine.

2. Open a python environment and move to the cloned directory 
```bash
    cd drive-scanner
```

3. Open ./config/config.ini and make sure you set some sensible defaults for database name, path and default search query. These defaults are particularly useful if you do many similar searches.

4. Scan your first drive
```bash
python main.py -n
```

This will option will guide you through the process with prompts. The database will be saved to whatever you set as the default in the config files. If you want to specify anything differently use the additional flags e.g.:

``` bash
python main.py -n --scan-dir /path/to/drive --drive-name MyDrive --db-path /path/to/database.db
```

Repeat this process for each new drive you want to save, making sure to use a unique drive name for each hard drive scanned.

5. Query the database using default query set in ./config/default_query.sql
```bash
python main.py -r
```

Or choose create a bespoke query if you prefer using this command, you will be prompted for the query
```bash
python main.py -r --query
```

This can be used with the previously demonstrated --db-path if you have a specific database you would like to use. 