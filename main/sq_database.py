import sqlite3
import pathlib
from pathlib import Path

main_path = pathlib.Path(__file__).parent.as_posix()
db_path = str(main_path) + "/main_data.db"
bd_path_checker = Path(db_path)

try:
    if bd_path_checker.is_file():
        print("db file found!")
    else:
        print("db file not found, making empty db!")
        open(db_path, 'a').close()
except IOError:
    print("Something is wrong with reading the database")

db_connection = sqlite3.connect(db_path)
db_cursor = db_connection.cursor()

def create_database_tables():
    sql_create_weather_today_table = '''CREATE TABLE IF NOT EXISTS weather_today (
                                    ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                                    temperature integer NOT NULL, 
                                    humidity integer NOT NULL, 
                                    solar integer NOT NULL, 
                                    hour integer NOT NULL, 
                                    date text NOT NULL)'''
    sql_create_weather_yesterday_table = '''CREATE TABLE IF NOT EXISTS weather_yesterday (
                                    ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                                    temperature integer NOT NULL, 
                                    humidity integer NOT NULL, 
                                    solar integer NOT NULL, 
                                    hour integer NOT NULL, 
                                    date text NOT NULL)'''

    db_cursor.execute(sql_create_weather_today_table)
    db_cursor.execute(sql_create_weather_yesterday_table)
    db_connection.commit()

def add_database_empty_data():
    sql_add_weather_today_data = '''INSERT INTO weather_today (
                                    temperature,
                                    humidity,
                                    solar,
                                    hour,
                                    date)
                                    VALUES(0,0,0,0,0)'''
    sql_add_weather_yesterday_data = '''INSERT INTO weather_yesterday (
                                    temperature,
                                    humidity,
                                    solar,
                                    hour,
                                    date)
                                    VALUES(0,0,0,0,0)'''

    db_cursor.execute(sql_add_weather_today_data)
    db_cursor.execute(sql_add_weather_yesterday_data)
    db_connection.commit()

def add_yesterday_database_data(data):
    sql_update_weather_yesterday_data = '''UPDATE weather_yesterday SET
                                    temperature = ?,
                                    humidity = ?,
                                    solar = ?,
                                    hour = ?,
                                    date = ?
                                    WHERE ID = ?'''
    for data in data:
        first_bit = data[0]
        shifted_data = [0,0,0,0,'0',0]
        for i in range (6):
            if i < 5:
                shifted_data[i] = data[i+1]
            else:
                shifted_data[i] = first_bit
        final_data = tuple(shifted_data)
        db_cursor.execute(sql_update_weather_yesterday_data, final_data)
        db_connection.commit()

def empty_today_database_data():
    sql_empty_today_data = '''UPDATE weather_today SET
                                    temperature = 0,
                                    humidity = 0,
                                    solar = 0,
                                    hour = 0,
                                    date = 0
                                    WHERE ID = ?'''
    for i in range(24):
        db_cursor.execute(sql_empty_today_data, (i+1,))
        db_connection.commit()

def update_database(data):
    sql_update_weather_today_data = '''UPDATE weather_today SET
                                    temperature = ?,
                                    humidity = ?,
                                    solar = ?,
                                    hour = ?,
                                    date = ?
                                    WHERE ID = ?'''

    db_cursor.execute(sql_update_weather_today_data, data)
    db_connection.commit()

def get_data_today():
    sql_get_weather_today_data = '''SELECT * FROM weather_today'''
    db_cursor.execute(sql_get_weather_today_data)
    return db_cursor.fetchall()

def get_data_yesterday():
    sql_get_weather_yesterday_data = '''SELECT * FROM weather_yesterday'''
    db_cursor.execute(sql_get_weather_yesterday_data)
    return db_cursor.fetchall()

def close_database_connection():
    db_connection.commit()
    db_connection.close()