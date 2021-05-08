import random
import mysql.connector

# list1 = list2 doesnt create a new list it just assings a new name to the inital list

class Password():#please look at encryption file this is outdated
	charsUpper=list(map(chr, range(65, 91)))
	charsLower=list(map(chr, range(97, 123)))
	alphabetLength=len(charsLower)

	def __init__(self, capitalChars =None, Chars=None, Numbers=None, Symbols=None, uncyphered=None, cyphered=None, step=None):

		self.capitalChars=capitalChars
		self.Chars=Chars
		self.Numbers=Numbers
		self.Symbols=Symbols
		self.uncyphered=uncyphered
		self.cyphered=cyphered
		self.step=step

	def generate(self):

		passList=[]

		for i in range(capitalChars):
			passList.append(random.choice(charsUpper))

		for i in range(Chars-capitalChars):
			passList.append(random.choice(charsLower))

		for i in range(Numbers):
			passList.append(random.randrange(0,9))

		for i in range(Symbols):
			passList.append(random.choice(['$','£','@','_']))	

		random.shuffle(passList)

		self.uncyphered=passList

	def Cypher(self):

		step=[]
		for i in range(self.Chars):
			step.append(random.randrange(0,alphabetLength))

		for i in range(self.Numbers):
			step.append(random.randrange(0,9))

		cyphered =[]
		shifted=0

		for i in range(self.capitalChars):
			shifted=(charsUpper.index(uncyphered[i]) +step[i])%(alphabetLength+1)
			cyphered.append(charsUpper[shifted])

		for i in range(self.Chars-self.capitalChars):
			shifted=(charsLower.index(uncyphered[i]) +step[i+self.capitalChars])%(alphabetLength+1)
			cyphered.append(charsLower[shifted])

		for i in range(self.Numbers):
			shifted=(uncyphered[i]+step[i+self.Chars])%10
			cyphered.append(shifted)

		self.step=step
		self.cyphered=cyphered

	def CountElements(self):
		#count the number of caps chars numbers and symbols

		symbols=len(self.cyphered)
		registered= False

		for letter in self.cyphered:
			registered=False

			for j in charsUpper:
				if letter == j:
					self.Chars+=1
					self.Symbols-=1
					registered = True

			if not registered:
				for j in range(9):
					if letter == j:
						self.Numbers+=1
						self.Symbols-=1

		
	def deCypher(self):
		#minus the key from the cyphered password  to get the uncyphered password.
		decrypted=[]
		shifted=0
		for i in range(self.capitalChars):
			shifted=charsUpper.index(cyphered[i]) -self.step[i]#negative indices start from the end of the list (i hope.)
			decrypted.append(charsUpper[shifted])

		for i in range(self.Chars-self.capitalChars):
			shifted=charsLower.index(cyphered[i]) -self.step[i+self.capitalChars]
			decrypted.append(charsLower[shifted])

		for i in range(self.Numbers):
			shifted=abs(cyphered[i]-step[i+self.Chars])
			decrypted.append(shifted)

		self.uncyphered=decrypted

def generatePasswordObject(mode, CapitalLetters = 0, Letters = 0, Numbers = 0, Symbols = 0, password = None):

	if mode == 'A':

		CapitalLetters= input('enter the number of capital letters :')
		Letters= input('enter the number of total letters :')
		Numbers= input('enter the number of numbers :')
		Symbols= input('enter the number of symbols :')
		UserPassword=Password(CapitalLetters,Letters,Numbers,Symbols)

	elif mode == 'S':

		UserPassword=Password(cyphered=password)
		UserPassword.CountElements()



	return UserPassword


def main():

	while True:

		choice1=input('press [A] to generate password \npress [S] to decypher a previous password (make sure you have your key) \npress [D] to load a saved password \npress [F] to Quit \n')
		if choice1== 'F':
			break

		service= input('enter the service for the password: ')
		cursor=databaseInteraction(service=service)

		if choice1== 'A':
			userPassword= generatePasswordObject(choice1)
			userPassword.generate()
			run=True
			output=''.join(userPassword.uncyphered)
			print(f'your password is: {output}')

			while run:
				choice2=input('press [A] to cypher password and save \npress [S] to save as is \npress [D] if you do not want to save this password \n')
				if choice2 == 'A':

					userPassword.cypher()
					key=''.join(userPassword.step)
					print(f'your key is {key}. please note this down ,as you will need it to access your password again')
					cursor.encrypted=''.join(userPassword.cyphered) #creates a string from the list 
					cursor.save()
					print('your password has been saved')

					run=False

				elif choice2== 'S':

					cursor.password = ''.join(userPassword.uncyphered)
					cursor.save()
					print('your password has been saved')

					run=False

				elif choice2== 'D':

					run=False


		elif choice1== 'S':

			userPassword= generatePasswordObject(choice1, password=list(cursor.loadCyphered()))
			key=input('enter your key :')
			userPassword.step=list(key)
			userPassword.deCypher()
			output= ''.join(userPassword.uncyphered)
			print(f'your password is: {output}')

		elif choice1== 'D':
			
			print(f'your password is: {cursor.loadPassword()}')

		# if statement for each choice: generate password gives option to save as is or cypher then save or dont save, decypher breaks loop

class databaseInteraction():

	def __init__(self,service=None,password=None,encrypted=None):#is none in python = to NULL in SQL???

		db= mysql.connector.connect(
			host='localhost',
			user='root',
			auth_plugin='mysql_native_password',
			database='Passwords',# database struct: PasswordForService (service VARCHAR(50), password VARCHAR(50), encrypted VARCHAR(50) DEFAULT NULL, PassID int PRIMARY KEY AUTO_INCREMENT )
			password='root'
			)


		self.cursor= db.cursor()

		self.service=service
		self.password=password
		self.encrypted=encrypted
	
	def save(self):
		try:
			self.cursor.execute('INSERT INTO PasswordForService (service,password,encrypted) VALUES (%s,%s,%s)',(self.service,self.password,self.encrypted))
		except:
			self.cursor.execute('DELETE FROM PasswordForService WHERE service= %s', (self.service))
			self.cursor.execute('INSERT INTO PasswordForService (service,password,encrypted) VALUES (%s,%s,%s)',(self.service,self.password,self.encrypted))

	def loadPassword(self):
		self.cursor.execute('SELECT password FROM PasswordForService WHERE service = %s', (self.service))
		return self.cursor[1]

	def loadCyphered(self):
		self.cursor.execute('SELECT cyphered FROM PasswordForService WHERE service = %s', (self.service))
		return self.cursor[1]


#good idea to make a GUI as to futher show skills.
