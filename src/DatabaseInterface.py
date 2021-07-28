import mysql.connector

class databaseInteraction():

	def __init__(self,user,masterPassword,service=None,password=None,encrypted=None):#is none in python = to NULL in SQL???

		self.db= mysql.connector.connect(
			host='localhost',
			user=user,
			database="Passwords",# database struct: PasswordForService (service VARCHAR(50) PRIMARY KEY, password VARCHAR(50), encrypted VARCHAR(50) DEFAULT NULL)
			password=masterPassword
			)


		self.cursor= self.db.cursor()

		self.service=service
		self.password=password
		self.encrypted=encrypted
	
	def save(self):
		try:
			self.cursor.execute('INSERT INTO PasswordForService (service,password,encrypted) VALUES (%s,%s,%s)',(self.service,self.password,self.encrypted))
		except:
			self.cursor.execute('DELETE FROM PasswordForService WHERE service= %s', (self.service,))
			self.cursor.execute('INSERT INTO PasswordForService (service,password,encrypted) VALUES (%s,%s,%s)',(self.service,self.password,self.encrypted))
		self.db.commit()

	def loadPassword(self):
		self.cursor.execute('SELECT password FROM PasswordForService WHERE service = %s', (self.service,))
		for x in self.cursor:
			return x[0]

	def loadCyphered(self):
		self.cursor.execute('SELECT encrypted FROM PasswordForService WHERE service = %s', (self.service,))
		for x in self.cursor:
			return x[0]