import sqlite3
import os
import sys
import glob
from tqdm import tqdm

def create_db(db_path):
    try:
        conn = sqlite3.connect(db_path)
        conn.execute('PRAGMA journal_mode = OFF;')  # Desactivar el journaling para mayor velocidad
        conn.execute('PRAGMA synchronous = OFF;')  # Reducir la sincronía para aumentar la velocidad de escritura
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

    except Exception as e:
        tqdm.write(f"Error creating database: {e}")
        sys.exit(1)

def insert_logs(conn, log_data):
    try:
        c = conn.cursor()

        c.executemany('''
            INSERT INTO logs (
                date, time, s_ip, cs_method, cs_uri_stem, cs_uri_query, s_port, cs_username,
                c_ip, cs_user_agent, cs_referer, sc_status, sc_substatus, sc_win32_status, time_taken
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', log_data)

        conn.commit()

    except Exception as e:
        tqdm.write(f"Error inserting logs: {e}")

def parse_log_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        data = []
        for line in lines:
            if not line.startswith('#'):
                parts = line.split()
                if len(parts) == 15:
                    data.append(tuple(parts))

        return data

    except Exception as e:
        tqdm.write(f"Error reading file {file_path}: {e}")
        return []

def process_logs(folder_path, db_path):

    conn = create_db(db_path)
    log_files = glob.glob(os.path.join(folder_path, '*.log'))

    if not log_files:
        tqdm.write("No log files found.")
        return

    pbar = tqdm(total=len(log_files), desc="Processing logs", unit="file")

    for log_file in log_files:
        pbar.set_description(f"File {os.path.basename(log_file)}")
        log_data = parse_log_file(log_file)

        if log_data:
            insert_logs(conn, log_data)

        pbar.update(1)

    conn.close()
    pbar.close()

    tqdm.write("Processing complete.")

if __name__ == "__main__":

    if len(sys.argv) != 3:
        tqdm.write("Usage: python script.py <folder_path> <db_path>")
        sys.exit(1)

    folder_path = sys.argv[1]
    db_path = sys.argv[2]

    process_logs(folder_path, db_path)
