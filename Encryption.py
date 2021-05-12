import random

class Password():
	charsUpper=list(map(chr, range(65, 91)))
	charsLower=list(map(chr, range(97, 123)))
	symbolList=['$','£','@','_']
	NumberOfSymbols=len(symbolList)
	alphabetLength=len(charsLower)

	def __init__(self, capitalChars =0, Chars=0, Numbers=0, Symbols=0, uncyphered=[], cyphered=[], step=[]):

		self.capitalChars=capitalChars
		self.Chars=Chars
		self.Numbers=Numbers
		self.Symbols=Symbols
		self.uncyphered=uncyphered
		self.cyphered=cyphered
		self.step=step

	def generate(self):

		passList=[]

		for i in range(self.capitalChars):
			passList.append(random.choice(self.charsUpper))

		for i in range(self.Chars-self.capitalChars):
			passList.append(random.choice(self.charsLower))

		for i in range(self.Numbers):
			passList.append(random.randrange(0,9))

		for i in range(self.Symbols):
			passList.append(random.choice(self.symbolList))	

		self.uncyphered=passList

	def Cypher(self):

		step=[]
		for i in range(self.Chars):
			step.append(random.randrange(0,self.alphabetLength))

		for i in range(self.Numbers):
			step.append(random.randrange(0,9))

		for i in range(self.Symbols):
			step.append(random.randrange(0,3))

		cyphered =[]
		shifted=0

		for i in range(self.capitalChars):
			shifted=(self.charsUpper.index(self.uncyphered[i]) +step[i])%(self.alphabetLength)
			cyphered.append(self.charsUpper[shifted])

		for i in range(self.Chars-self.capitalChars):
			shifted=(self.charsLower.index(self.uncyphered[i+self.capitalChars]) +step[i+self.capitalChars])%(self.alphabetLength)
			cyphered.append(self.charsLower[shifted])

		for i in range(self.Numbers):
			shifted=(self.uncyphered[i+self.Chars]+step[i+self.Chars])%10
			cyphered.append(shifted)

		for i in range(self.Symbols):
			shifted=(self.symbolList.index(self.uncyphered[i+self.Chars+self.Numbers])+step[i+self.Chars+self.Numbers])%self.NumberOfSymbols
			cyphered.append(self.symbolList[shifted])

		self.step=step
		self.cyphered=cyphered

	def CountElements(self):
		#count the number of caps chars numbers and symbols

		registered= False

		for letter in self.cyphered:
			registered=False
			for j in self.charsUpper:
				if letter == j:
					self.capitalChars+=1
					registered = True
					print('char counted')

			if not registered:
				for j in self.charsLower:
					if letter == j:
						self.Chars+=1
						registered= True
						print('capital char counted')

			if not registered:
				for j in range(9):
					if letter == j:
						self.Numbers+=1
						print('int counted')

		symbols=len(self.cyphered)-(self.capitalChars+self.Chars+self.Numbers)


	def deCypher(self):
		#minus the key from the cyphered password  to get the uncyphered password.
		decrypted=[]
		shifted=0
		for i in range(self.capitalChars):
			shifted=self.charsUpper.index(self.cyphered[i]) -self.step[i]#negative indices start from the end of the list (i hope.)
			decrypted.append(self.charsUpper[shifted])

		for i in range(self.Chars-self.capitalChars):
			shifted=self.charsLower.index(self.cyphered[i+self.capitalChars]) -self.step[i+self.capitalChars]
			decrypted.append(self.charsLower[shifted])

		for i in range(self.Numbers):
			shifted=abs(self.cyphered[i+self.Chars]-self.step[i+self.Chars])
			decrypted.append(shifted)


		for i in range(self.Symbols):
			shifted=self.symbolList.index(self.cyphered[i+self.Chars+self.Numbers])-self.step[i+self.Chars+self.Numbers]
			decrypted.append(self.symbolList[shifted])


		self.uncyphered=decrypted

	#new function that randomly shuffles self.shuffleIndex= range(0,len(password)-1) and uses a for loop to rearrange the uncyphered list into a new random order  
	#new function that uses the shuffle index and a nest for loop to rearange the shuffled list back into an ordered version
CapitalLetters= 1
Letters= 3
Numbers= 2
Symbols= 1
UserPassword=Password(capitalChars=CapitalLetters,Chars=Letters,Numbers=Numbers,Symbols=Symbols)
print(UserPassword.charsUpper)
UserPassword.generate()
print(UserPassword.uncyphered)
UserPassword.Cypher()
print(UserPassword.cyphered)
UserPassword.deCypher()
print(UserPassword.uncyphered)

newPassword=Password(cyphered=['T', 'o', 'r', 1, 1])
newPassword.CountElements()
print([newPassword.Chars,newPassword.capitalChars,newPassword.Numbers,newPassword.Symbols])