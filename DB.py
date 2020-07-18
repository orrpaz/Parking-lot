import mysql.connector
import configparser


def readconfig():
    config = configparser.RawConfigParser()
    config.read('./config.properties')
    details_dict = dict(config.items('SECTION_NAME'))
    return details_dict


def create_db():
    mydb = connect_db()
    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE IF NOT EXISTS parking")
    mydb.connect(database="parking")
    mycursor.execute("CREATE TABLE IF NOT EXISTS log (lisence VARCHAR(255), allowed VARCHAR(255), info VARCHAR(255),"
                     "timer  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
                     " PRIMARY KEY(lisence) )")
    mycursor.close()
    mydb.close()


def connect_db():
    details_dict = readconfig()
    mydb = mysql.connector.connect(
        host=details_dict['host'],
        user=details_dict['user'],
        password=details_dict['password'],
        auth_plugin=details_dict['auth_plugin']
    )
    return mydb

def insert_db(query,val):

    mydb = connect_db()
    mycursor = mydb.cursor()
    mycursor.execute(query, val)
    mydb.commit()
    mycursor.close()
    mydb.close()


