#!/bin/bash
############################################################################################
##                                    install.sh                                          ##
##                              Author: Arjun Bhatia                                      ##
##                             Copyright 2022 Artemis IX                                  ##
##                  This script installs all the dependencies on the AMI                  ##
## 1. Upgrade the OS packages.                                                            ##
## 2. Install all the application prerequisites, middleware, and runtime.                 ##
## 3. Install MySQL and setup the database.                                          ##
## 4. Update permission and file ownership on the copied application artifacts.           ##
## 5. Start the REST API service                                                          ##
############################################################################################

echo "+-----------------------------------------------------------------------------------------------------------------------------------------+"
echo "|                                                                                                                                         |"
echo "|                                                           INSTALL SCRIPT v1.0                                                           |"
echo "|                                                                                                                                         |"
echo "+-----------------------------------------------------------------------------------------------------------------------------------------+"
sudo yum Update
# Install zip and unnzip
echo "+-----------------------------------------------------------------------------------------------------------------------------------------+"
echo "|                                                                                                                                         |"
echo "|                                                         Installing zip and unzip                                                        |"
echo "|                                                                                                                                         |"
echo "+-----------------------------------------------------------------------------------------------------------------------------------------+"
sudo yum install zip -y
sudo yum install unzip -y

# Install Python
echo "+-----------------------------------------------------------------------------------------------------------------------------------------+"
echo "|                                                                                                                                         |"
echo "|                                                         Installing Python                                                         |"
echo "|                                                                                                                                         |"
echo "+-----------------------------------------------------------------------------------------------------------------------------------------+"
sudo yum install python3

# Install 
echo "+-----------------------------------------------------------------------------------------------------------------------------------------+"
echo "|                                                                                                                                         |"
echo "|                                                              Installing PIP                                                             |"
echo "|                                                                                                                                         |"
echo "+-----------------------------------------------------------------------------------------------------------------------------------------+"
curl -O https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py --user


echo "+-----------------------------------------------------------------------------------------------------------------------------------------+"
echo "|                                                          DATABASE OPERATIONS                                                            |"
echo "+-----------------------------------------------------------------------------------------------------------------------------------------+"
echo "|                                                                                                                                         |"
echo "|                                                         Installing MYSQL                                                           |"
echo "|                                                                                                                                         |"
echo "+-----------------------------------------------------------------------------------------------------------------------------------------+"

# echo "+-----------------------------------------------------------------------------------------------------------------------------------------+"
# echo "|                                                                                                                                         |"
# echo "|                                                     Boostrapping PostgreSQL database                                                    |"
# echo "|                                                                                                                                         |"
# echo "+-----------------------------------------------------------------------------------------------------------------------------------------+"
# sudo su postgres <<EOF
# createdb test;
# psql -c "CREATE ROLE me WITH LOGIN PASSWORD 'password';"
# EOF
# BOOTPSQL=$?
# if [ $BOOTPSQL -eq 0 ]; then
#   echo "Postgres User 'me' and database 'test' created successfully!"
# else
#   echo "Unable to Boostrap the PostgreSQL database"
# fi

echo "+-----------------------------------------------------------------------------------------------------------------------------------------+"
echo "|                                                                                                                                         |"
echo "|                                                   Validating Installed Package Versions                                                 |"
echo "|                                                                                                                                         |"
echo "+-----------------------------------------------------------------------------------------------------------------------------------------+"
echo "python $(python3 --version)"
echo "pip $(pip --version)"


echo "+-----------------------------------------------------------------------------------------------------------------------------------------+"
echo "|                                                                                                                                         |"
echo "|                                                          Validating Binaries                                                            |"
echo "|                                                                                                                                         |"
echo "+-----------------------------------------------------------------------------------------------------------------------------------------+"

/usr/bin/pip3 install boto3
/usr/bin/pip3 install flask
/usr/bin/pip3 install mysql-connector-python
/usr/bin/pip3 install bcrypt
/usr/bin/pip3 install SQLAlchemy
/usr/bin/pip3 install databases
/usr/bin/pip3 install pymysql
/usr/bin/pip3 install requests
/usr/bin/pip3 install python-dotenv
/usr/bin/pip3 install statsd
/usr/bin/pip3 install http.client
/usr/bin/pip3 install uuid

echo "+-----------------------------------------------------------------------------------------------------------------------------------------+"
echo "|                                                                                                                                         |"
echo "|                                                            Unpacking Artifacts                                                          |"
echo "|                                                                                                                                         |"
echo "+-----------------------------------------------------------------------------------------------------------------------------------------+"
unzip /home/ec2-user/webapp.zip -d /home/ec2-user/
sleep 3
sudo rm -rf /home/ec2-user/webapp.zip
sleep 3
echo "+-----------------------------------------------------------------------------------------------------------------------------------------+"
echo "|                                                                                                                                         |"
echo "|                                                         Installing app dependencies                                                     |"
echo "|                                                                                                                                         |"
echo "+-----------------------------------------------------------------------------------------------------------------------------------------+"
cd webapp

sudo mv app.service /etc/systemd/system/webapp.service
