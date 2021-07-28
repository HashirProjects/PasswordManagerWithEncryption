import mysql.connector# make sure to pip install mysql.connector.python not just mysql.connector

def main(user,masterPassword):
	db= mysql.connector.connect(
		host='localhost',
		user=user,
		password=masterPassword
		)

	cursor= db.cursor()
	#cursor.execute('CREATE DATABASE Passwords') #use this code to create the database


	db= mysql.connector.connect(
		host='localhost',
		database='passwords',
		user=user,
		password=masterPassword
		)

	cursor= db.cursor()
	#cursor.execute('CREATE TABLE PasswordForService (service VARCHAR(50) PRIMARY KEY, password VARCHAR(50), encrypted VARCHAR(50) DEFAULT NULL )')
	#the above creates an empty table

	def test():
		testText= 'test'
		cursor.execute('INSERT INTO PasswordForService (service,password,encrypted) VALUES (%s,%s,%s)',(testText,testText,testText))
		#use db.commit() after you make a change to your database if you want it to save!

		cursor.execute('SELECT password FROM PasswordForService WHERE service = %s', ("google",))

		for x in cursor:
			print(x)
		print(cursor)

	test()

if __name__ == "__main__":
	main("root","root")

