import mysql.connector
import traceback
import getpass
import sys
import pandas as pd

class CreateDB:
	def __init__(self):
		try:            
			self.conn = mysql.connector.connect(host="localhost",user="root",password="root")
			self.cur = self.conn.cursor()
			self.cur.execute("CREATE DATABASE IF NOT EXISTS ShoppingCart")
		except Exception as e:
			print(e)

class Project:
	
	def __init__ (self):
		"""Initialize db class variables"""
		try:
			self.connection = mysql.connector.connect(host="localhost",user="root",password="root",database="ShoppingCart")
			self.cursor = self.connection.cursor()          
		except Exception as e:
			print(e)
	def commit(self):
		"""commit changes to database"""
		self.connection.commit()    

	def connection_close(self):
		"""close sqlite3 connection"""
		self.connection.close()


# ---------------------------------CUSTOMER REGISTER TABLE-----------------------------------------------------

	def customer_insert(self):
		try:
			print("Please Fill the details")
			print("--------------------------------")
			customer_name1 = input("ENTER YOUR NAME ")
			customer_age1 = input("ENTER YOUR AGE  ")
			customer_phone_no1 = int(input("ENTER YOUR PHONE NUMBER "))
			customer_address1 = input("ENTER YOUR ADDRESS ")
			customer_email_id1 = input("ENTER YOUR EMAIL ID ")
			customer_pass1 = getpass.getpass(prompt='ENTER YOUR PASSWORD ')
			raw_sql="INSERT INTO customer(customer_name,customer_age,customer_phone_no,customer_address,customer_email_id,customer_password) values(%s,%s,%s,%s,%s,%s)"
			sql_args = (customer_name1 ,customer_age1 ,customer_phone_no1,customer_address1, customer_email_id1,customer_pass1)
		
			self.cursor.execute(raw_sql, sql_args)
			print("Successfully Registered.")
			print("------------------------------")
			print("Now For login Please Enter your Valid details")
			self.customer_login()
			self.commit()
		except Exception as e:
			print(e)
		finally:
			self.connection_close() 

# ---------------------------------CUSTOMER LOGIN TABLE-----------------------------------------------------

	def customer_login(self):
		try:
			customer_email_id = input("ENTER EMAIL ID : ")
			customer_pass = getpass.getpass(prompt='ENTER YOUR PASSWORD : ')
			self.cursor.execute("SELECT customer_id FROM customer WHERE customer_email_id = %s AND customer_password = %s ",(customer_email_id,customer_pass))
			customer_check = self.cursor.fetchone()
			print(customer_check,"55555")
			if customer_check:
				customer_id = customer_check[0]				
				if customer_email_id == 'admin@gmail.com':
					self.admin_accesbilty()                
				else:
					self.product_view_for_customer(customer_id)
			else:
				print("Invalid Username or Password!!")             
		except Exception as e:
			raise
					   
# ---------------------------------CUSTOMER CREATE TABLE-----------------------------------------------------

	def customer_create(self): 
		try:
			self.cursor.execute(''' SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'customer' ''')
			if self.cursor.fetchone()[0] !=1:
				raw_sql = "CREATE TABLE customer(customer_id INT AUTO_INCREMENT PRIMARY KEY, customer_name VARCHAR(255),customer_age INT(3) NOT NULL,customer_phone_no INT(11) NOT NULL ,customer_address VARCHAR(255) ,customer_email_id VARCHAR(255) NOT NULL UNIQUE , customer_password VARCHAR(10) NOT NULL)"      
				self.cursor.execute(raw_sql)
				raw_sql_admin="INSERT INTO customer(customer_name,customer_age,customer_phone_no,customer_address,customer_email_id,customer_password) values(%s,%s,%s,%s,%s,%s)"
				sql_args_admin = ("Admin",25,789654123,"Indore MP","admin@gmail.com","Admin1234")		
				self.cursor.execute(raw_sql_admin, sql_args_admin)		
				self.commit()
				print("Record created successfully.")
				print("------------------------------")
			self.customer_insert()									
		except Exception as e:
			print(traceback.print_exc())        

# ---------------------------------PRODUCT CREATE TABLE-----------------------------------------------------

	def product_create(self):
		try:
			print("create product table")
			self.cursor.execute(''' SELECT count(*) FROM information_schema.tables WHERE table_name = 'product' ''')
			if self.cursor.fetchone()[0] !=1:
				raw_sql = "CREATE TABLE product(product_id INT AUTO_INCREMENT PRIMARY KEY, product_name VARCHAR(255) NOT NUll, product_detail VARCHAR(255) NOT NULl , product_price INT(5))"
				self.cursor.execute(raw_sql)
				print("Record created successfully.")
				print("------------------------------")
				self.commit()
			else:
				print("Table already created")
		except Exception as e:
			print(traceback.print_exc())
		# finally:
		#     self.connection_close()

#------------------------------------ PRODUCT INSERT TABLE ------------------------------------------- 

	def product_insert(self):
		print("Please Enter the details")
		print("--------------------------------")
		try:
			pro_name = input("Enter the product name :")
			pro_detail = input("enter the product details:")
			pro_price = int(input("enter the price of a product:"))
			raw_sql = "INSERT INTO product(product_name ,product_detail , product_price) VALUES (%s,%s,%s)"
			sql_args = (pro_name,pro_detail,pro_price)
			self.cursor.execute(raw_sql, sql_args)
			print("Record inserted successfully.")
			print("------------------------------")
			self.commit()
		except Exception as e:
			print(e)
		# finally:
		#     self.connection_close()

#------------------------------------ SHOW PRODUCT LIST -------------------------------------------

	def product_view(self):
		print("Product List")       
		try:
			raw_sql = "SELECT * FROM product"
			self.cursor.execute(raw_sql)
			records = self.cursor.fetchall()
			print(records) 
			self.commit()
		except Exception as e:
				print(e)  
			
		# finally:
		#     self.connection_close()


#------------------------------------ UPDATE PRODUCT DETAILS -------------------------------------------

	def product_update(self):
		try:
			pro_id = input("enter the id of a product :")
			pro_name = input("enter the product name :")
			pro_detail = input("enter the product details :")
			pro_price = input("enter the price of a product :")
			res = "SELECT * FROM product WHERE product_id=%s"
			res_id = (pro_id,)
			raw_select =self.cursor.execute(res, res_id)
			product_record = self.cursor.fetchone()
			if product_record:
				pro_name = pro_name or product_record[1]
				pro_detail = pro_detail or product_record[2]
				pro_price = pro_price or product_record[3]
				raw_sql = "UPDATE product SET product_name = %s, product_price = %s, product_detail = %s WHERE product_id = %s"
				sql_args = (pro_name, pro_price, pro_detail, pro_id,)
				self.cursor.execute(raw_sql, sql_args) 
				self.commit()
				print("Record updated successfully.")
			else:
				print ("Product for given id does not exist in databse")
		except Exception as e:
			print(e)        		

#------------------------------------ DELETE PRODUCT -------------------------------------------

	def product_delete(self):

		try:
			pro_id = int(input(" enter the product id :"))
			raw_res = "SELECT * FROM product WHERE product_id=%s"
			raw_set =self.cursor.execute(raw_res,(pro_id,))
			product_record = self.cursor.fetchone()   
			if product_record == None:
				print("Product for given id does not exist in database")  
			else:
				raw_sql = "DELETE  FROM product WHERE product_id=%s"
				var = self.cursor.execute(raw_sql,(pro_id,))
				print("Record deleted  successfully.")     
			self.commit()
		except Exception as e:
			print(e)		

#------------------------------------ SALE ORDER LINE TABLE --------------------------------

	def order_line_create(self):
		try:
			self.cursor.execute(''' SELECT count(*) FROM information_schema.tables WHERE table_name = 'order_line' ''')
			if self.cursor.fetchone()[0] !=1:
				raw_sql = "CREATE TABLE order_line(new_product_id INT(10), customer_id INT(10), product_price INT(20), product_quantity real NOT NULl  DEFAULT 1.00, sub_total real not null, FOREIGN KEY (customer_id) REFERENCES customer(customer_id))"
				self.cursor.execute(raw_sql)
				print("Record created successfully.")
				print("------------------------------")
				self.commit()  
		except Exception as e:
			print(traceback.print_exc())

#------------------------------------ ADD TO CART TABLE --------------------------------

	def add_to_cart_create(self):
		try:
			self.cursor.execute(''' SELECT count(*) FROM information_schema.tables WHERE table_name = 'add_to_cart' ''')
			if self.cursor.fetchone()[0] !=1:
				raw_sql = "CREATE TABLE add_to_cart(product_name VARCHAR(255) NOT NUll, product_detail VARCHAR(255) NOT NULl , product_price INT(5))"
				self.cursor.execute(raw_sql)
				print("Record created successfully.")
				print("------------------------------")
				self.commit()  
		except Exception as e:
			print(traceback.print_exc())
					
# ---------------------------------------CREATE ALL TABLES-------------------------------------
   
	def create_tables(self):
		self.customer_create()
		self.product_create()
		self.order_line_create()
		self.add_to_cart_create()
	
	def order_history(self,customer_id):
		try:
			ids = []
			product_name = []
			product_details = []
			product_price = []				
			raw_sql = self.cursor.execute("SELECT * FROM order_line WHERE customer_id = %s", (customer_id,))
			select_product = self.cursor.fetchall()			            
			for row in select_product:
				ids.append(row[0]) 
				product_name.append(row[1])
				product_details.append(row[2])
				product_price.append(row[3])
			
			data = {
					'ID':ids,
					'Product Name': product_name,
					'Details': product_details,
					'Price': product_price
			}
			df_1 = pd.DataFrame(data)
			print(df_1)				
			self.commit()  
		except Exception as e:
			print(e)



#------------------------------------ PRODUCT LIST -------------------------------------------

	def  product_view_for_customer(self,customer_id):
		"""Show Product List"""       
		try:
			ids = []
			product_name = []
			product_details = []
			product_price = []
			raw_sql = "SELECT * FROM product"
			self.cursor.execute(raw_sql)
			records = self.cursor.fetchall()
			for rec in records:
				ids.append(rec[0]) 
				product_name.append(rec[1])
				product_details.append(rec[2])
				product_price.append(rec[3])
			data = {
					'ID':ids,
					'Product Name': product_name,
					'Details': product_details,
					'Price': product_price
					}				

			df = pd.DataFrame(data)
			print(df)				
			self.commit()
		except Exception as e:
				print(e)          
		print("1 : Buy Product --")
		print("2 : Add To Cart--")
		print("3 : Order History--")
		print("4 : Logout---")
		choice = int(input("Enter choice"))
		if choice == 1:
			project_db.buy_product(customer_id)
		elif choice == 2:
			project_db.add_to_cart()
		elif choice == 3:
			project_db.order_history(customer_id)			
		else:
			project_db.exit()

#------------------------------------ BUY PRODUCT -------------------------------------------

	def buy_product(self,customer_id):
		try:     
			# while True:
			valid_product_id = input("For Buying Products Please Enter Product valid ID's--")
			valid_product_id_set = set(valid_product_id.split(','))
			for ids in valid_product_id_set:  
				raw_sql =self.cursor.execute("select * from product where product_id =%s",(ids,))
				select_product = self.cursor.fetchone()
				if select_product:
					pro_id = ids
					pro_price = select_product[3]
					print("For ID ",ids, "Enter qunatity = ")
					qunatity = int(input())
					sub_total= qunatity * pro_price
					raw_sql1="insert into order_line(new_product_id,customer_id,product_price,product_quantity,sub_total) values(%s,%s,%s,%s,%s)"
					raw_args1 = (pro_id,customer_id,pro_price, qunatity, sub_total)
					self.cursor.execute(raw_sql1,raw_args1)
				else:
					print(ids,"is not available in the product list.")
				self.order_line_show()
				self.commit()
		except Exception as e:
			print(traceback.print_exc())
		

#------------------------------------ SHOW ORDER LINE TABLE -------------------------------------------

	def order_line_show(self):
		try:
			raw_sql = self.cursor.execute("SELECT * FROM order_line")
			select_product = self.cursor.fetchall()
			print('-' *150, "\nProduct_id\tProduct_Price\tQuantity\tSub_total\n", '-' *150)            
			for row in select_product:
				print(row)
				print("\n")
				 
			self.commit()  
		except Exception as e:
			print(e)

#------------------------------------ ADD PRODUCT INTO CART -------------------------------------------

	def add_to_cart(self):
		try:
			valid_product_id = input("For Buying Products Please Enter Product valid ID's--")
			valid_product_id_set = set(valid_product_id.split(','))
			for ids in valid_product_id_set :  
				raw_sql =self.cursor.execute("select * from product where product_id =%s",(ids,))
				select_product = self.cursor.fetchone()
				if select_product:
					pro_name = select_product[1]
					pro_detail =select_product[2]
					pro_price = select_product[3]
					raw_sql1="insert into add_to_cart(product_name,product_detail,product_price) values(%s,%s,%s)"
					raw_args1 = (pro_name,pro_detail,pro_price)
					self.cursor.execute(raw_sql1,raw_args1)
					raw_sql = self.cursor.execute("SELECT * FROM add_to_cart")
					select_product = self.cursor.fetchall()
					print('-' *150, "\nProduct_Name\tProduct_details\tProduct_Price\n", '-' *150)            
					for row in select_product:
						print(row)

						print("\n")
				 
				self.commit()
		except Exception as e:
			print(e)

# ------------------------------------ADMIN LOGIN----------------------------------------------
   
	def admin_accesbilty(self):
			while True:
				print(" 1:---------------for insert product -------------")
				print(" 2:---------------for view product----------------")
				print(" 3:---------------for update product--------------")
				print(" 4:---------------for delete product--------------")
				print(" 5:---------------for create tables---------------")
				print(" 6:---------------for logout------------------------")
				choice = int(input("Enter choice"))
				if choice == 5:
					project_db.create_tables()
				elif choice == 1:
					project_db.product_insert()
				elif choice == 2:
					project_db.product_view()
				elif choice == 3:
					project_db.product_update()
				elif choice == 4:
					project_db.product_delete()
				elif choice == 6:
					project_db.exit()
				else:
					pass

	def exit(self):		
		sys.exit()

db_create = CreateDB()
project_db = Project()

print("1 :----------LOGIN-------------")
print("2 :----------CUSTOMER REGISTRATION----")

choice1 = int(input("enter the choice"))
if choice1 == 1:
	project_db.customer_login()
elif choice1 == 2:
	project_db.customer_insert()