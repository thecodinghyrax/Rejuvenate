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
                                        esoui_id text DEFAULT "",
                                        folder_name text NOT NULL,
                                        web_name text NOT NULL,
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


def insert_addon(addon):
    """Create a new addon for table
    :param conn: The SQLite connection object
    :param addon: A tuple of a addon (name, )
    :return: addon id
    """
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        sql = """ INSERT INTO addon (esoui_id,name,updated)
                VALUES(?,?,?) """
        cur.execute(sql, addon)
        conn.commit()
        return cur.lastrowid  # returns the row id of the cursor object, the addon id


def get_all_addons():
    """Query all rows of addon table
    :param conn: The SQLite connection object
    :return: All rows containing data from the addon table
    """
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT esoui_id,name,search_name,updated,version,user_updated FROM addon")
    rows = cur.fetchall()

    return rows  # return the rows

def get_one_addon(field, value):
    """Query a single row of the addon table
    :param conn: The SQLite connection object
    :return: All rows containing data from the addon table
    """
    conn = create_connection()
    cur = conn.cursor()
    sql = f"""SELECT esoui_id,name,search_name,updated,version,user_updated,installed 
                FROM addon
                WHERE {field} GLOB '{value}*'"""
    cur.execute(sql)
    row = cur.fetchone()

    return row  # return the row

def get_matching_addons(field, value):
    """Query a single row of the addon table
    :param conn: The SQLite connection object
    :return: All rows containing data from the addon table
    """
    conn = create_connection()
    cur = conn.cursor()
    sql = f"""SELECT esoui_id,name,search_name,updated,version,user_updated,installed 
                FROM addon
                WHERE {field} GLOB '{value}*'"""
    cur.execute(sql)
    row = cur.fetchall()
    return row

def update_one_addon(search_field, search_name, update_field, new_data):
    conn = create_connection()
    cur = conn.cursor()
    if type(new_data) == int:
        sql = f"""UPDATE addon SET {update_field}={new_data}, user_updated=1
                WHERE {search_field}='{search_name}'"""
    else:
        sql = f"""UPDATE addon SET {update_field}='{new_data}', user_updated=1
                 WHERE {search_field}='{search_name}'"""
    try:
        cur.execute(sql)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

def update_addon_by_id(esoui_id, field, new_value):
    conn = create_connection()
    cur = conn.cursor()
    if type(new_value) == int:
        sql = f"""UPDATE addon SET {field}={new_value} WHERE esoui_id='{esoui_id}'"""
    else:
        sql = f"""UPDATE addon SET {field}='{new_value}' WHERE esoui_id='{esoui_id}'"""
    try:
        cur.execute(sql)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False


def update_addons_from_list(search_field, search_list, update_field, new_data_list):
    pass


def set_all_to_uninstalled():
    conn = create_connection()
    cur = conn.cursor()
    sql = f"""UPDATE addon SET installed=0 WHERE installed=1"""
    try:
        cur.execute(sql)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False



if __name__ == "__main__":
    pass