import base64
from distutils.log import error
import email
import errno
from http.client import BAD_REQUEST
from multiprocessing.connection import wait
from flask import abort, request, make_response
import requests
from assignment import app
from database import SqlAlchemy as mysql
from flask import jsonify
import pymysql
import re

# from werkzeug.security import generate_password_hash
from datetime import datetime

import bcrypt
import logging

# logging.basicConfig(level=logging.DEBUG)

s = b'$2b$12$5bLd8.tAyVOYX66Y2KLNROtA86OappyUFvMtpSYsMDGnH2z1HNnUO'


@app.route('/v1/user', methods=['POST'])
def create_user():
	csr = None
	db_error = False
	try:
		js = request.json
		username = js['username']
		password = js['password']
		fname = js['first_name']
		lname = js['last_name']

		# validate the received values
	

		if not re.match(r"[^@]+@[^@]+\.[^@]+", username):
			return jsonify({'error': 'Invalid email address'}), 400

		hash_pwd = bcrypt.hashpw(password.encode('utf-8'), s)
		# datetime object containing current date and time
		u_crdate = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

		query = "INSERT INTO tbl_create_user(username, u_password, u_fname, u_lname, acc_created, acc_updated) VALUES(%s, %s, %s, %s, %s, %s)"
		field = (username, hash_pwd, fname, lname, u_crdate, u_crdate)

		csr = mysql.cursor()
		csr.execute(query, field)
		mysql.commit()

		query = "SELECT u_id, username, u_fname, u_lname, acc_created, acc_updated FROM tbl_create_user WHERE username = %s"
		field = (username,)
		csr.execute(query, field)

		keys = [column[0] for column in csr.description]
		data = csr.fetchone()
		result = dict(zip(keys, data))
		result = jsonify(result)
		result.status_code = 201
		return result

	except Exception as e:
		db_error = True
	finally:
		if csr:
			csr.close()
	if db_error:
		result = jsonify(Error="BAD_REQUEST", Code=400)
		result.status = 400
		return result


# @app.route('/v1/user', methods=['POST'])
# def create_user():

# 	#dbcon =None
# 	csr =None

# 	try:

# 		js = request.json
# 		username =js['username']
# 		password =js['password']
# 		fname =js['fname']
# 		lname=js['lname']

# 		# datetime object containing current date and time
# 		now = datetime.now()

# 		# dd/mm/YY H:M:S
# 		u_crdate = now.strftime('%Y-%m-%dT%H:%M:%S.%f%z')


# 		# validate the received values
# 		if fname and lname and username and password and request.method == 'POST':
# 			if not re.match(r"[^@]+@[^@]+\.[^@]+", username):
# 				return jsonify({'error': 'Invalid email address'}),400

# 			# bcrypt password
# 			bytes = password.encode('utf-8')
# 			# salt = bcrypt.gensalt()
# 			hash_pwd = bcrypt.hashpw(bytes, s)

# 			# insert data into db
# 			query = "INSERT INTO tbl_create_user(username, u_password, u_fname, u_lname,acc_created,acc_updated) VALUES(%s,%s,%s,%s,%s,%s)"
# 			field = (username,hash_pwd,fname,lname,u_crdate,u_crdate)

# 			# # connect with mysql
# 			# #dbcon = mysql.connect()
# 			csr = mysql.cursor()

# 			# # execute the query
# 			csr.execute(query, field)

# 			mysql.commit()

# 			# rows = csr.fetchone()
# 			csr.close()	

# 			csr = mysql.cursor()

# 			query = "SELECT u_id,username,u_fname,u_lname,acc_created,acc_updated from tbl_create_user where username= %s"
# 			field = (username,)
# 			csr.execute(query, field)
# 			keys = [column[0] for column in csr.description]
# 			data=csr.fetchone()
# 			result = dict(zip(keys, data))
# 			result = jsonify(result)

# 			# result = jsonify('User added successfully!',201)
# 			result.status_code = 201

# 			return result
# 		else:
# 			#dbcon = mysql.connect()
# 			csr = mysql.cursor()
# 			return not_found()
# 	# except mysql.connector.Error:
# 	# 	print("error duplicacy")
# 	except Exception as e:
# 		# print(e)
# 		db_error=True		
# 		# dbcon = mysql.connect()
# 		# csr = dbcon.cursor()

# 	finally:
# 		#dbcon = mysql.connect()
# 		csr = mysql.cursor()
# 		csr.close() 
# 		#dbcon.close()

# 	if db_error:
# 		# print("duplicate error")
# 		result=jsonify(Error="BAD_REQUEST", Code = 400  )	
# 		result.status=400

# 		# return jsonify((400, 'Record Not Found')) 
# 		# result.status_code="400 BAD_REQUEST"
# 		return result

# @app.route('/v1/user',methods=['GET'])
# def users():

@app.route('/v1/user/<int:Id>')
def user(Id):
	# dbcon = None
	csr = None
	try:
		# js = request.json
		# Id =js['id']

		if Id:

			# dbcon = mysql.connect()

			csr = mysql.cursor()
			query = "Select u_id from tbl_create_user where u_id=%s"
			field = (Id,)
			csr.execute(query, field)

			rec = csr.fetchone()

			if (rec is None):

				csr.close()
				result = jsonify("Not Found", 404)
				result.status_code = 404

				return result
			else:
				csr.close()

				# skipping first 6 digits
				auth_token = str(request.headers['Authorization'])[6:]
	
				check_auth = authenticate_user(auth_token)
				db_uid= check_auth
				if check_auth != False:
				
					if(db_uid==Id):
					
						print("matched")
						csr = mysql.cursor()
						query = "SELECT u_id,username,u_fname,u_lname,acc_created,acc_updated from tbl_create_user where u_id=%s"
						field = (Id,)
						csr.execute(query, field)
						# field = (email)
						keys = [column[0] for column in csr.description]

						exist = csr.fetchone()
						if exist is None:
							raise logging.exception
					
						result = dict(zip(keys, exist))
						result = jsonify(result)
						result.status_code = 200
						return result
					else:
						result = jsonify("Forbidden", 403)
						result.status_code = 403
						return result
				else:
					result = jsonify("Unauthorized", 401)
					result.status_code = 401
					return result
				
	except Exception:
		db_error = True
	# result=jsonify(Error="Bad_Request-No details found", Code = 400  )
	# result.status=400
	# result.status_code=400
	# print(e)
	finally:

		csr.close()
	# dbcon.close()
	if db_error:
		# print("duplicate error")
		result = jsonify(Error="Bad Request", Code=400)
		result.status_code = 400

		
		return result


# healthzz api
@app.route("/healthz")
def myname():
	return jsonify({"Application is healthy": "200"})


# update api
@app.route('/v1/user/<int:Id>', methods=['PUT'])
def update_user(Id):
	# dbcon = None
	csr = None
	db_error=False
	try:
		js = request.json
		user_name = js['username']
		u_password = js['password']
		fname = js['first_name']
		lname = js['last_name']
	except Exception:
		db_error = True
	if db_error:
		result = jsonify(Error="BAD_REQUEST", Code=400)
		result.status_code = 400
		return result

	expected_keys = ["username", "password", "fname", "lname"]
	extra_keys = set(js.keys()) - set(expected_keys)

	if extra_keys:
		resp = jsonify({"message": "Bad Request! because you cannot update u_id, account_created or account_updated"})
		resp.status_code = 400
		return resp


	try:


		# datetime object containing current date and time
		now = datetime.now()

		# dd/mm/YY H:M:S
		u_update = now.strftime('%Y-%m-%dT%H:%M:%SZ')
		

		# validate the received values
		if expected_keys and request.method == 'PUT':

			# dbcon=mysql.connect()
			csr = mysql.cursor()
			query = "Select u_id from tbl_create_user where u_id=%s and username =%s "
			field = (Id, user_name)
			csr.execute(query, field)

			rec = csr.fetchone()

			if (rec is None):

				csr.close()
				result = jsonify("Bad_Request", 400)
				result.status_code = 400

				return result
			else:

				csr.close()

				# skipping first 6 digits
				auth_token = str(request.headers['Authorization'])[6:]
				
				check_auth = authenticate_user(auth_token)
				db_uid= check_auth
				if check_auth != False:
				
					if(db_uid==Id):

						print("matched")
						csr = mysql.cursor()
					# bcrypt password
						bytes = u_password.encode('utf-8')
						hashed_pwd = bcrypt.hashpw(bytes, s)

					# save edits
						sql = "UPDATE tbl_create_user SET u_fname=%s, u_lname=%s, u_password=%s, acc_updated=%s WHERE u_id=%s"
						data = (fname, lname, hashed_pwd, u_update, Id)
					# dbcon = mysql.connect()
						csr = mysql.cursor()

						csr.execute(sql, data)
						mysql.commit()
					# print(csr.rowcount)
						if csr.rowcount == 0:
							raise logging.exception
							print("csr is none")
					# exist = csr.fetchone()
					# if exist is not None:

						result = jsonify('User updated successfully!')
						result.status_code = 204
						return result
					else:
						result = jsonify("Forbidden", 403)
						result.status_code = 403
						return result
				else:
					# dbcon = mysql.connect()
					csr = mysql.cursor()
					result = jsonify("Unauthorized User", 401)
					result.status_code = 401
					return result

	except Exception as e:
		# print(e)
		# dbcon = mysql.connect()
		csr = mysql.cursor()
		result = jsonify(Error="Bad_Request", Code=400)

		result.status_code = 400
		return result
	# # resp = jsonify("User can't be updated!")
	# # resp.status_code = 404
	# # return result
	# # print(e)
	finally:
		csr.close()


# dbcon.close()

@app.route('/v1/product', methods=['POST'])
def upload_product():
	# if 'files[]' not in request.files:
	# 	resp=jsonify({'message': 'No file is found'})
	# 	resp.status_code=400
	# 	return resp
	data = request.json
	product_name = data.get("name")
	product_description = data.get("description")
	product_sku = data.get("sku")
	product_manufacturer = data.get("manufacturer")
	product_quantity = data.get("quantity")
	int(product_quantity)
	csr = None
	

# errors={}
	success = False
	auth_token = str(request.headers['Authorization'])[6:]
	
	check_auth = authenticate_user(auth_token)
	
	
# print(check_auth)
	try:
		if not product_name or not product_description or not product_sku or not product_manufacturer or not product_quantity or  request.method != 'POST':
			raise Exception
		elif check_auth != False:
			u_id = check_auth
			now = datetime.now()
			print(now)
			u_created = now.strftime('%Y-%m-%dT%H:%M:%SZ')

			if product_quantity and int(product_quantity) >=0:
				
				query = "INSERT INTO tbl_product(P_name, description, sku, Manufacturer,Quantity,Date_added,Date_last_update,u_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
				field = (product_name, product_description, product_sku, product_manufacturer, product_quantity, u_created,u_created,u_id)
				csr = mysql.cursor()
				csr.execute(query, field)
				mysql.commit()
				query = "SELECT p_id, P_name, description, sku, Manufacturer, Quantity,Date_added, Date_last_update,u_id FROM tbl_product WHERE u_id = %s"
				field = (u_id,)
				csr.execute(query,field)
				result=[]

				records = csr.fetchall()
				for rec in records:
					keys = [column[0] for column in csr.description]
					values = rec
					record_dict = dict(zip(keys, values))
					result.append(record_dict)

				result = jsonify(result)
				result.status_code = 201
				csr.close()
				return result
			else:
				return 'Quantity cannot be less than 0', 400

	# success=True
		else:

			resp = jsonify({'message': 'Authorization Error'})
			resp.status_code = 401
			return resp
	except Exception as e:
			success = True
	if success:
		resp = jsonify({"Bad Request": "400"})
		resp.status_code = 400
		return resp
# else:
#     resp=jsonify({'message':'File type is exceeding the size or multiple files are not allowed'})
#     resp.status_code=400
#     return resp

def authenticate_user(auth_token):
	csr = None
	# print("entered auth method")
	# print(auth_token)
	try:
		csr = mysql.cursor()
		# auth_token=str(request.headers['Authorization'])[6:]
		# print("1")
		auth_token1 = base64.b64decode(auth_token)

		auth_split = str(auth_token1).split(':')
		auth_uname = str(auth_split[0])[2:]
		
		# print(auth_uname)
		auth_pwd = str(auth_split[1])
		

		hash_pwd = pwd(auth_pwd[:-1])
		

		query = "Select u_password pwd,u_id from tbl_create_user where username=%s"
		field = (auth_uname,)
		csr.execute(query, field)
		rec = csr.fetchone()

		db_pwd = rec[0]
		db_uid = rec[1]
		# print(db_pwd)
		# print(db_uid)
		# except Exception:
		#     result=jsonify("Unauthorized user", Code = 401  )
		#     result.status_code=401
		#     return False

		if (rec is None):

			csr.close()
			result = jsonify("Unauthorized user", 401)
			result.status_code = 401
			return False
		else:
			csr.close()

			if ((str(hash_pwd)[2:].replace('\'', '') == db_pwd)):
				print("matched")
				return db_uid
			else:
				# csr.close()
				result = jsonify("Unauthorized user", 401)
				result.status_code = 401
				return False

	except Exception as e:
		db_error = True
		# print(e)
	# finally:
@app.route('/v1/product/<int:P_Id>', methods=['DELETE'])
def delete_product(P_Id):
	csr = None
	
	
# errors={}
	success = False
	auth_token = str(request.headers['Authorization'])[6:]
	csr = mysql.cursor()
	query = "Select P_id from tbl_product where P_id=%s"
	field = (P_Id,)
	csr.execute(query, field)

	rec = csr.fetchone()

	if (rec is None):

				csr.close()
				result = jsonify("Not Found", 404)
				result.status_code = 404

				return result
	else:
		check_auth = authenticate_user(auth_token)
		u_id = check_auth
		try:
			csr = mysql.cursor()
			query = "Select P_id from tbl_product where P_id=%s and u_id=%s"
			field = (P_Id,u_id)
			csr.execute(query, field)

			rec = csr.fetchone()

			if check_auth != False:

				
				if (rec is not None):
			
				
				


					query = "DELETE FROM tbl_product where p_id =%s and u_id=%s"
					field = (P_Id, u_id)
					csr = mysql.cursor()
					csr.execute(query, field)
					mysql.commit()
					result = jsonify("No Content", 204)
					result.status_code = 204
					return result
			
				else:
					raise Exception
					
			else:
				resp = jsonify({'message': 'Authorization Error'})
				resp.status_code = 401
				return resp 

		except Exception as e:
				success = True
		if success:
			resp = jsonify({"Forbidden": "403"})
			resp.status_code = 403
			return resp


@app.route('/v1/product/<int:P_Id>', methods=['PUT'])
def update_product(P_Id):
	csr = None
	data = request.json
	product_name = data.get("name")
	product_description = data.get("description")	
	product_sku = data.get("sku")
	product_manufacturer = data.get("manufacturer")
	product_quantity = data.get("quantity")
	
	
	
	expected_keys = ["p_name", "description", "sku", "manufacturer", "product_quantity"]
	extra_keys = set(data.keys()) - set(expected_keys)

	if extra_keys:
		resp = jsonify({"message": "Bad Request! because you cannot update p_id, date_added,date_last_updated or u_id"})
		resp.status_code = 400
		return resp
	if not product_name or not product_description or not product_sku or not product_manufacturer or not product_quantity or  request.method != 'PUT':
		resp = jsonify({"message": "Bad Request! You need to enter product_name, product_description, product_sku, product_manufacturer, product_quantity"})
		resp.status_code = 400
		return resp

	csr = mysql.cursor()
	query = "Select P_id,u_id from tbl_product where P_id=%s"
	field = (P_Id,)
	csr.execute(query, field)
	rec = csr.fetchone()
		
	csr.close()	
	if rec==None:
		result = jsonify("Not Found", 404)
		result.status_code = 404

		return result
	db_pid = rec[0]
	db_uid = rec[1]
# errors={}
	
	success = False
	auth_token = str(request.headers['Authorization'])[6:]
	
	check_auth = authenticate_user(auth_token)
	now = datetime.now()
	u_update = now.strftime('%Y-%m-%dT%H:%M:%SZ')
	u_id = check_auth
	try:
		if check_auth != False:
			if (u_id == db_uid):
				if product_quantity and int(product_quantity) >= 0:
					
		
					query = "UPDATE tbl_product SET P_name=%s, description=%s, sku=%s, Manufacturer=%s, Quantity= %s,Date_last_update=%s WHERE u_id=%s and p_id=%s"
					field = (product_name,product_description,product_sku,product_manufacturer,product_quantity,u_update, u_id,P_Id)
					csr = mysql.cursor()
					csr.execute(query, field)
					mysql.commit()
					query = "SELECT p_id, P_name, description, sku, Manufacturer, Quantity,Date_added, Date_last_update,u_id FROM tbl_product WHERE u_id = %s"
					field = (u_id,)
					csr.execute(query,field)
					result=[]
					records = csr.fetchall()
					for rec in records:
						keys = [column[0] for column in csr.description]
						values = rec
						record_dict = dict(zip(keys, values))
						result.append(record_dict)

					result = jsonify(result)
					result.status_code = 204
					csr.close()
					return result
				else:
					return 'Quantity cannot be less than 0', 400
			else:
				resp = jsonify({'message': 'Forbidden'})
				resp.status_code = 403
				return resp
			 
		else:

			resp = jsonify({'message': 'Authorization Error'})
			resp.status_code = 401
			return resp
	except Exception as e:
		success = True
	if success:
		resp = jsonify({"Bad Request": "400"})
		resp.status_code = 400
		return resp

@app.route('/v1/product/<int:P_Id>', methods=['PATCH'])
def update_product_patch(P_Id):
	csr = None
	data = request.json
	product_name = data.get("name")
	if product_name is None:
		csr = mysql.cursor()
		query = "SELECT P_name FROM tbl_product WHERE p_id = %s"
		field = (P_Id,)
		csr.execute(query, field)
		product_name = csr.fetchone()[0]
		csr.close()


	product_description = data.get("description")
	if product_description is None:
		csr = mysql.cursor()
		query = "SELECT description FROM tbl_product WHERE p_id = %s"
		field = (P_Id,)
		csr.execute(query, field)
		product_description = csr.fetchone()[0]
		csr.close()


	product_sku = data.get("sku")
	if product_sku is None:
		csr = mysql.cursor()
		query = "SELECT sku FROM tbl_product WHERE p_id = %s"
		field = (P_Id,)
		csr.execute(query, field)
		product_sku = csr.fetchone()[0]
		csr.close()


	product_manufacturer = data.get("manufacturer")
	if product_manufacturer is None:
		csr = mysql.cursor()
		query = "SELECT Manufacturer FROM tbl_product WHERE p_id = %s"
		field = (P_Id,)
		csr.execute(query, field)
		product_manufacturer = csr.fetchone()[0]
		csr.close()


	product_quantity = data.get("quantity")
	if product_quantity is None:
		csr = mysql.cursor()
		query = "SELECT  Quantity FROM tbl_product WHERE p_id = %s"
		field = (P_Id,)
		csr.execute(query, field)
		product_quantity = csr.fetchone()[0]
		csr.close()
	
	
	
	expected_keys = ["p_name", "description", "sku", "manufacturer", "product_quantity"]
	extra_keys = set(data.keys()) - set(expected_keys)

	if extra_keys:
		resp = jsonify({"message": "Bad Request! because you cannot update p_id, date_added,date_last_updated or u_id"})
		resp.status_code = 400
		return resp
	if not product_name or not product_description or not product_sku or not product_manufacturer or not product_quantity or  request.method != 'PATCH':
		resp = jsonify({"message": "Bad Request! You need to enter product_name, product_description, product_sku, product_manufacturer, product_quantity"})
		resp.status_code = 400
		return resp

	csr = mysql.cursor()
	query = "Select P_id,u_id from tbl_product where P_id=%s"
	field = (P_Id,)
	csr.execute(query, field)
	rec = csr.fetchone()
	
	csr.close()	
	if rec==None:
		result = jsonify("Not Found", 404)
		result.status_code = 404

		return result
	db_pid = rec[0]
	db_uid = rec[1]
# errors={}
	
	success = False
	auth_token = str(request.headers['Authorization'])[6:]
	
	check_auth = authenticate_user(auth_token)
	now = datetime.now()
	u_update = now.strftime('%Y-%m-%dT%H:%M:%SZ')
	u_id = check_auth
	try:
		if check_auth != False:
			if (u_id == db_uid):
				if product_quantity and int(product_quantity) >= 0:
					
		
					query = "UPDATE tbl_product SET P_name=%s, description=%s, sku=%s, Manufacturer=%s, Quantity= %s,Date_last_update=%s WHERE u_id=%s and p_id=%s"
					field = (product_name,product_description,product_sku,product_manufacturer,product_quantity,u_update, u_id,P_Id)
					csr = mysql.cursor()
					csr.execute(query, field)
					mysql.commit()
					query = "SELECT p_id, P_name, description, sku, Manufacturer, Quantity,Date_added, Date_last_update,u_id FROM tbl_product WHERE u_id = %s"
					field = (u_id,)
					csr.execute(query,field)
					result=[]
					records = csr.fetchall()
					for rec in records:
						keys = [column[0] for column in csr.description]
						values = rec
						record_dict = dict(zip(keys, values))
						result.append(record_dict)

					result = jsonify(result)
					result.status_code = 204
					csr.close()
					return result
				else:
					return 'Quantity cannot be less than 0', 400
			else:
				resp = jsonify({'message': 'Forbidden'})
				resp.status_code = 403
				return resp
			 
		else:

			resp = jsonify({'message': 'Authorization Error'})
			resp.status_code = 401
			return resp
	except Exception as e:
		success = True
	if success:
		resp = jsonify({"Bad Request": "400"})
		resp.status_code = 400
		return resp

@app.route('/v1/product/<int:P_Id>',methods=['GET'])
def get_product(P_Id):
	if P_Id:

			# dbcon = mysql.connect()

			csr = mysql.cursor()
			query = "Select p_id from tbl_product where p_id=%s"
			field = (P_Id,)
			csr.execute(query, field)

			rec = csr.fetchone()

			if (rec is None):

				return not_found()
			else:
				csr = mysql.cursor()
				query = "SELECT p_id, P_name, description, sku, Manufacturer, Quantity,Date_added, Date_last_update,u_id FROM tbl_product WHERE  p_id=%s"
				field = (P_Id,)
				csr.execute(query,field)
				data = csr.fetchone()
				keys = [column[0] for column in csr.description]
				result = dict(zip(keys, data))
				result = jsonify(result)
				result.status_code = 200
				csr.close()
				return result
		
	
@app.errorhandler(404)
def not_found(error=None):
	message = {
		'status': 404,
		'message': 'Not Found: ',
	}
	resp = jsonify(message)
	resp.status_code = 404

	return resp




def pwd(password):
	pd = password.encode('utf-8')
	return bcrypt.hashpw(pd, s)


if __name__ == "__main__":
	app.run()

#((str(hash_pwd)[2:].replace('\'', '') == db_pwd) and (auth_uname == db_uname))