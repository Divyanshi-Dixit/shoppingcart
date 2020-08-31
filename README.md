Shopping Cart   
This sample application demonstrates a simple shopping cart built with python-mysql. It contains three services, a shopping cart service, for managing shopping carts, and managing customer order history.    
The shopping cart service persist customer can buy a product and add their product into order list and one more service provided, a customer can add their item into cart in case of buying that product later.   
Order histroy service is like a customer can see his/her previouse data/purchase-order in the form of excel sheet on console.   
 
Setup  
 To run this application locally you will need follow some pre-requisites     
-This application is based on python3 so you should have python installed in your system in case it is not installed this is link for installation of python.  
 https://phoenixnap.com/kb/how-to-install-python-3-ubuntu    
-Install MYSQL.connector for database connectivity.   
 python -m pip install mysql-connector-python   
-Install Pandas for Dataframes.   
 sudo pip install pandas    
 We suggest you to run it on python virtual environment or you can run locally with above installation steps.    
 create virtual enviornment for python3 on ubuntu    
 python3 -m venv env-name    
 source env-name/bin/activate   
 After successfully activating enviornment run requirement.txt .  
	
 Steps to Use Application   
 after running file , there are two choices are displyed over console     
 1-For login    
 2-For registration.   
   
 Admin access-   
 Firstly for admin accessibility admin need to choose 2 option so there will create a customer table and admin will be registered automatically.   
 Then admin need to login.   
 credentials - EmailId = admin@gmail.com , Password = 123@admin   
 Roles of Admin-   
 1.Can see all the products and add/delete products.   
 Roles of User(customer)-  
 1.Can browse all the products.   
 2.Can purchase any product in any amout of quantity.   
 2.Add products into the cart.   
 3.Can Check his/her order history.   
 
 
 

 
 
 
 




