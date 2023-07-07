import sqlite3

def add_group_to_database(id: str, title: str, type: str):
    sqlite_connection = sqlite3.connect('DB_data.db')
    cursor = sqlite_connection.cursor()
    insert_group_into_database = f"INSERT INTO group_data (id, title, type) VALUES ('{id}', '{title}', '{type}')"
    cursor.execute(insert_group_into_database)
    sqlite_connection.commit()

def get_chat_ids():
    sqlite_connection = sqlite3.connect('DB_data.db')
    cursor = sqlite_connection.cursor()
    select_id_from_database = "SELECT id from group_data"
    data_temp = cursor.execute(select_id_from_database).fetchall()
    data = [each[0] for each in data_temp]
    return data

def delete_group_from_database(title: str):
    sqlite_connection = sqlite3.connect('DB_data.db')
    cursor = sqlite_connection.cursor()
    delete_group_from_database = f"DELETE FROM group_data WHERE title = '{title}'"
    cursor.execute(delete_group_from_database)
    sqlite_connection.commit()

def is_admin_here(user_name: str):
    sqlite_connection = sqlite3.connect('DB_data.db')
    cursor = sqlite_connection.cursor()
    delete_group_from_database = f"SELECT * FROM admins WHERE user_name = '{user_name}'"
    if cursor.execute(delete_group_from_database).fetchone() == None:
        return False
    else:
        return True

def add_admin_to_database(user_name: str):
    sqlite_connection = sqlite3.connect('DB_data.db')
    cursor = sqlite_connection.cursor()
    insert_admin_to_database = f"INSERT INTO admins (user_name) VALUES ('{user_name}')"
    cursor.execute(insert_admin_to_database)
    sqlite_connection.commit()

def delete_admin_from_database(user_name: str):
    sqlite_connection = sqlite3.connect('DB_data.db')
    cursor = sqlite_connection.cursor()
    delete_admin_from_database = f"DELETE FROM admins WHERE user_name = '{user_name}'"
    cursor.execute(delete_admin_from_database)
    sqlite_connection.commit()

def parse_group_chat_ids_into_arr():
    sqlite_connection = sqlite3.connect('DB_data.db')
    cursor = sqlite_connection.cursor()
    select_group_chat_ids_from_database = "SELECT id FROM group_data"
    arr_of_ids = [each[0] for each in cursor.execute(select_group_chat_ids_from_database).fetchall()]
    return arr_of_ids

def parse_group_chat_titles_into_arr():
    sqlite_connection = sqlite3.connect('DB_data.db')
    cursor = sqlite_connection.cursor()
    select_group_chat_titles_from_database = "SELECT title FROM group_data"
    arr_of_titles = [each[0] for each in cursor.execute(select_group_chat_titles_from_database).fetchall()]
    return arr_of_titles

def chat_id_by_title_group(title: str):
    sqlite_connection = sqlite3.connect('DB_data.db')
    cursor = sqlite_connection.cursor()
    select_group_by_title_in_database = f"SELECT id FROM group_data WHERE title = '{title}'"
    answer = cursor.execute(select_group_by_title_in_database).fetchone()[0]
    return answer