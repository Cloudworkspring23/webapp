Building Rest API using Python. MySQL and Flask

This is a python web application for storing the user information into MySQL database.

User input is taken from Postman

User passwords are encrypted with BCrypt hashing and salt in the database

Authentication is done using basic auth

This API implements GET,POST,PUT and Delete methods

The infrasturucture files ami.pkr.hcl is used to create custom AMI with all the dependency required to build and start the web application. The AMI file is automatically build in the GitHub action workflows.

Clone the AWS INFRA repository and run the Terraform Command:
1. Terraform init
2. Terraform fmt
3. Terraform Plan -var-file="demo.tfvars"
4. Terraform Apply -var-file="demo.tfvars"


Call the API using Postman
User input is taken from Postman
