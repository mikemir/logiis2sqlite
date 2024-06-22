import duckdb
import os
import sys
import glob
from tqdm import tqdm

def create_db(db_path):
    conn = duckdb.connect(db_path)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            date VARCHAR,
            time VARCHAR,
            s_ip VARCHAR,
            cs_method VARCHAR,
            cs_uri_stem VARCHAR,
            cs_uri_query VARCHAR,
            s_port INTEGER,
            cs_username VARCHAR,
            c_ip VARCHAR,
            cs_user_agent VARCHAR,
            cs_referer VARCHAR,
            sc_status INTEGER,
            sc_substatus INTEGER,
            sc_win32_status INTEGER,
            time_taken INTEGER
        )
    ''')
    return conn

def insert_logs(conn, log_data):
    conn.executemany('''
        INSERT INTO logs (
            date, time, s_ip, cs_method, cs_uri_stem, cs_uri_query, s_port, cs_username,
            c_ip, cs_user_agent, cs_referer, sc_status, sc_substatus, sc_win32_status, time_taken
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', log_data)

def parse_log_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
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
        insert_logs(conn, log_data)
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <folder_path> <db_path>")
        sys.exit(1)
    folder_path = sys.argv[1]
    db_path = sys.argv[2]
    process_logs(folder_path, db_path)
