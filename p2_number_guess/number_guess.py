# Number Guessing
# Use the random module to help generate the random number
import random
# randint() will generate a random integer between 1-100, assign it to 'number'
number = random.randint(1,100)
# guess will store the guesses that the user makes
guess = 0
# continue the game until the user guesses correctly
while guess != number:
  guess = int(input("Enter Guess: "))
  
  if (guess < number):
    print("Guess higher!")
  elif (guess > number):
    print("Guess lower!")
  else:
    print("You won!")
