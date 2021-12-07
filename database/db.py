import sqlite3
from sqlite3 import Error
import constants



def create_connection():
    """Connect to a SQLite database
    :db: filename of database
    :return connection if no error, otherwise None"""
    try:
        conn = sqlite3.connect(constants.DB_NAME)
        return conn
    except Error as err:
        print(err)
    return None


def create_table(sql_create_table):
    """Creates table with given sql statement
    :param conn: Connection object
    :param sql_create_table: a SQL CREATE TABLE statement
    :return:
    """
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute(sql_create_table)
    except Error as e:
        print(e)


def create_tables():
    """ Create all tables for the db
    :returns: Nothing. Message is printed if connection error
    """
    sql_create_web_addon_table = """ CREATE TABLE IF NOT EXISTS web_addon (
                                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                        esoui_id text NOT NULL,
                                        name text NOT NULL,
                                    ); """
    sql_create_local_addon_table = """ CREATE TABLE IF NOT EXISTS local_addon (
                                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                        esoui_id text DEFAULT '',
                                        folder_name text NOT NULL,
                                        web_name text DEFAULT '',
                                        loacl_version text DEFAULT '0',
                                        web_version text DEFAULT '0',
                                    ); """
    # create a database connection
    conn = create_connection()
    if conn is not None:
        create_table(sql_create_web_addon_table)
        create_table(sql_create_local_addon_table)
    else:
        print("Unable to connect to the database")


def insert_web_addon(addon):
    """Create a new addon for table
    :param conn: The SQLite connection object
    :param addon: A tuple of a addon (esoui_id, name)
    :return: addon id
    """
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        sql = f""" INSERT INTO local_addon (esoui_id,name)
                VALUES(?,?) """
        cur.execute(sql, addon)
        conn.commit()
        return cur.lastrowid  # returns the row id of the cursor object, the addon id

def insert_local_addon(addon):
    """Create a new addon for table
    :param conn: The SQLite connection object
    :param addon: local_folder name for the addon
    :return: addon id
    """
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        sql = f""" INSERT INTO web_addon (folder_name)
                VALUES(?) """
        cur.execute(sql, (addon))
        conn.commit()
        return cur.lastrowid  # returns the row id of the cursor object, the addon id



def get_all_web_addons():
    """Query all rows of the web_addon table
    :return: All rows containing data from the web_addon table
    """
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT esoui_id,name FROM web_addon")
    rows = cur.fetchall()
    

def get_all_local_addons():
    """Query all rows of the local_addon table
    :return: All rows containing data from the local_addon table
    """
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT esoui_id,folder_name,web_name,local_version,web_version FROM local_addon")
    rows = cur.fetchall()
    return rows 

def get_one_addon(table, field, value):
    """Query a single row of the requested table
    :param field: The column to search
    :param value: The desired value of the field
    :return: A single row from the table
    """
    conn = create_connection()
    cur = conn.cursor()
    if type(value) == int:
         sql = f"""SELECT *
                FROM {table}
                WHERE {field}=={value}"""   
    else:
        sql = f"""SELECT *
                    FROM {table}
                    WHERE {field}=='{value}'"""
    cur.execute(sql)
    row = cur.fetchone()
    return row  # return the row


def update_one_addon(table, search_field, search_name, update_field, new_data):
    '''Update one row of the db
    :param table: The table to update
    :param search_field: The column to match in the WHERE clause
    :param search_name: The value to match in the WHERE clause
    :param update_field: The column to update
    :param new_data: The new value to add to the column
    :returns: True if successful, False if there was an exception'''
    conn = create_connection()
    cur = conn.cursor()
    if type(new_data) == int:
        sql = f"""UPDATE {table} SET {update_field}={new_data}, user_updated=1
                WHERE {search_field}='{search_name}'"""
    else:
        sql = f"""UPDATE {table} SET {update_field}='{new_data}', user_updated=1
                 WHERE {search_field}='{search_name}'"""
    try:
        cur.execute(sql)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

def update_addon_by_id(table, esoui_id, field, new_value):
    '''Update one row of the db using the usoui_id
    :param table: The table to update
    :param esoui_id: The esoui_id from the website
    :param field: The column to update
    :param new_value: The new value to add to the column
    :returns: True if successful, False if there was an exception'''
    conn = create_connection()
    cur = conn.cursor()
    if type(new_value) == int:
        sql = f"""UPDATE {table} SET {field}={new_value} WHERE esoui_id='{esoui_id}'"""
    else:
        sql = f"""UPDATE {table} SET {field}='{new_value}' WHERE esoui_id='{esoui_id}'"""
    try:
        cur.execute(sql)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False



if __name__ == "__main__":
    pass