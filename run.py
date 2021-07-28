from src.PasswordGen import Password
from src.DatabaseInterface import databaseInteraction

def generatePasswordObject(mode, CapitalLetters = 0, Letters = 0, Numbers = 0, Symbols = 0, password = None):#Untested

	if mode == 'A':

		CapitalLetters= input('enter the number of capital letters :')
		Letters= input('enter the number of total letters :')
		Numbers= input('enter the number of numbers :')
		Symbols= input('enter the number of symbols :')
		UserPassword=Password(capitalChars=CapitalLetters,Chars=Letters,Numbers=Numbers,Symbols=Symbols)

	elif mode == 'S':

		UserPassword=Password(cyphered=password)
		UserPassword.CountElements()

	return UserPassword

def main():

	while True:
		user=input("enter your database username: ")
		masterPassword=input("enter your database password: ")

		try:
			cursor=databaseInteraction(user, masterPassword)
			break
		except:
			print("those details were incorrect, please try again\n")

	while True:

		choice1=input('\npress [A] to generate password \npress [S] to decypher a previous password (make sure you have your key) \npress [D] to load a saved password \npress [F] to Quit \n')
		if choice1== 'F':
			break

		service= input('enter the service which the password is for: ')
		cursor.service=service

		if choice1== 'A':
			userPassword= generatePasswordObject(choice1)
			userPassword.generate()
			run=True
			output=''.join(userPassword.uncyphered)#turns the list into a string (not neccecary but easier to look at)
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

			userPassword=Password(cyphered=list(cursor.loadCyphered()))
			userPassword.CountElements()

			key=input('enter your key :')
			userPassword.step=list(key)
			userPassword.deCypher()
			output= ''.join(userPassword.uncyphered)
			print(f'your password is: {output}')

		elif choice1== 'D':
			
			print(f'your password is: {cursor.loadPassword()}')

		# if statement for each choice: generate password gives option to save as is or cypher then save or dont save, decypher breaks loop

if __name__ == "__main__":
	main()