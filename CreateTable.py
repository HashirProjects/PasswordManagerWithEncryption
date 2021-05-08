import mysql.connector# make sure to pip install mysql.connector.python not just mysql.connector


db= mysql.connector.connect(
	host='localhost',
	user='root',
	auth_plugin='mysql_native_password',# new version needs this parameter passed you might not see in tutorials
	database='Passwords',
	password='root'
	)

cursor= db.cursor()
#cursor.execute('CREATE TABLE PasswordForService (service VARCHAR(50) PRIMARY KEY, password VARCHAR(50), encrypted VARCHAR(50) DEFAULT NULL )')
testText= 'test'
#cursor.execute('INSERT INTO PasswordForService (service,password,encrypted) VALUES (%s,%s,%s)',(testText,testText,testText))
#use db.commit() after you make a change to your database

cursor.execute('SHOW TABLES')

for x in cursor:
	print(x)

