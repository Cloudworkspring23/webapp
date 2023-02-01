import mysql.connector
from flask import jsonify
# from flaskext.mysql import MySQL


def getDbConnection():


    mydb = mysql.connector.connect(
    host='127.0.0.1',
    user="new_user",
    password="password"
    )

    mycursor = mydb.cursor()

    mycursor.execute("Create Database If NOt EXISTS clouddb")
    mycursor.close()

def createTable():
    mydb = mysql.connector.connect(
    host="localhost",
    user="new_user",
    password="password",
    database="clouddb",
    auth_plugin='mysql_native_password'
    )
    mycursor = mydb.cursor()
    mycursor.execute("CREATE TABLE IF NOT EXISTS tbl_Create_User(u_id bigint Auto_Increment Primary Key,username varchar(45) Unique, u_password varchar(255) DEFAULT NULL,u_fname varchar(45)  DEFAULT NULL,u_lname varchar(45)  DEFAULT NULL,acc_created varchar(45)  DEFAULT NULL,acc_updated varchar(45) DEFAULT NULL) ENGINE=InnoDB AUTO_INCREMENT=1")
    mycursor.close()



getDbConnection()
createTable()
SqlAlchemy = mysql.connector.connect(host="localhost",user="new_user",password="password",database="clouddb")

