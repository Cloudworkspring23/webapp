import requests
import database
from flask import Flask as flsk
app = flsk(__name__)

database.getDbConnection()
database.createTable()
database.createTable_product()
