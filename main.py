import sqlite3
import os
import sys
import glob
from tqdm import tqdm

def create_db(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            date TEXT,
            time TEXT,
            s_ip TEXT,
            cs_method TEXT,
            cs_uri_stem TEXT,
            cs_uri_query TEXT,
            s_port INTEGER,
            cs_username TEXT,
            c_ip TEXT,
            cs_user_agent TEXT,
            cs_referer TEXT,
            sc_status INTEGER,
            sc_substatus INTEGER,
            sc_win32_status INTEGER,
            time_taken INTEGER
        )
    ''')
    conn.commit()
    return conn

def insert_log(conn, log_data):
    c = conn.cursor()
    c.execute('''
        INSERT INTO logs (
            date, time, s_ip, cs_method, cs_uri_stem, cs_uri_query, s_port, cs_username,
            c_ip, cs_user_agent, cs_referer, sc_status, sc_substatus, sc_win32_status, time_taken
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', log_data)
    conn.commit()

def parse_log_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        data = []
        for line in lines:
            if not line.startswith('#'):
                parts = line.split()
                if len(parts) == 15:
                    data.append(tuple(parts))
        return data

def process_logs(folder_path, db_path):
    conn = create_db(db_path)
    log_files = glob.glob(os.path.join(folder_path, '*.log'))
    for log_file in tqdm(log_files, desc="Processing logs", unit="file"):
        log_data = parse_log_file(log_file)
        for entry in tqdm(log_data, desc=f"Inserting records from {os.path.basename(log_file)}", leave=False, unit="record"):
            insert_log(conn, entry)
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <folder_path> <db_path>")
        sys.exit(1)
    folder_path = sys.argv[1]
    db_path = sys.argv[2]
    process_logs(folder_path, db_path)
