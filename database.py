import mysql.connector
from flask import jsonify
# from flaskext.mysql import MySQL
from dotenv import load_dotenv
from pathlib import Path
import os

dotenv_path = Path("/home/ec2-user/webapp/.env")
load_dotenv(dotenv_path=dotenv_path)
db_name=os.environ.get('DB_DATABASE')
db_host=os.environ.get('DB_HOST')
db_user = os.environ.get('DB_USER')
db_pass = os.environ.get('DB_PASSWORD')
# def getDbConnection():


    # mydb = mysql.connector.connect(
    # host="db_host",
    # user="DB_User",
    # password="DB_Pass"
    # )

    # mycursor = mydb.cursor()
    # mycursor.execute("SHOW DATABASES")
    # databases = mycursor.fetchall()
    # database_names = [database[0] for database in databases]



    # mycursor.execute("Create Database If NOt EXISTS clouddb")
    # mycursor.close()

def createTable():
    mydb = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_pass,
    database=db_name,
    )
    mycursor = mydb.cursor()
    mycursor.execute("CREATE TABLE IF NOT EXISTS tbl_create_user(u_id bigint Auto_Increment Primary Key,username varchar(45) Unique, u_password varchar(255) DEFAULT NULL,u_fname char(45)  DEFAULT NULL,u_lname char(45)  DEFAULT NULL,acc_created varchar(45)  DEFAULT NULL,acc_updated varchar(45) DEFAULT NULL) ENGINE=InnoDB AUTO_INCREMENT=1")
    mycursor.close()

def createTable_product():
    mydb = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_pass,
    database=db_name
    )
    mycursor = mydb.cursor()
    mycursor.execute("CREATE TABLE if not exists tbl_product(p_id bigint Auto_Increment Primary Key,P_name varchar(45) DEFAULT NULL,description varchar(100) DEFAULT NULL,sku varchar(10) Unique,Manufacturer varchar(20) DEFAULT NULL,Quantity bigint,Date_added varchar(50) Default Null,Date_last_update varchar(50),u_id bigint, foreign key(u_id) references tbl_create_user(u_id) )ENGINE=InnoDB AUTO_INCREMENT=1")
    mycursor.close()

def createTable_image():
    mydb = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_pass,
    database=db_name
    )
    mycursor = mydb.cursor()
    mycursor.execute("CREATE TABLE if not exists tbl_image(image_id bigint Auto_Increment Primary Key,p_id bigint ,file_name varchar(100) DEFAULT NULL,Date_created varchar(50) Default Null,s3_bucket_path varchar(200),foreign key(p_id) references tbl_product(p_id) )ENGINE=InnoDB AUTO_INCREMENT=1")
    mycursor.close()


# getDbConnection()
createTable()
createTable_product()
createTable_image()
SqlAlchemy = mysql.connector.connect(host=db_host,user=db_user,password=db_pass,database=db_name)

