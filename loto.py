from random import randint
from random import shuffle
from random import choice
from debug_log import log

class Loto():
	'''
	Class loto allows to delete number from card and displays a card
	Method __init__ doesn't take arguments and creates a card according to loto rules.
	Card is a list of 3 lists (rows) randomly filled with blanks and numbers.
	'''

	all_numbers = list( range(1,91) )
	shuffle(all_numbers)

	def __init__(self):
		def randomizer(spisok):
			'''
			Has one argument - list. Returns a random element from this list and removes it from the list
			'''
			result = choice(spisok)
			spisok.remove(result)
			return result

		# CREATE TEMPLATE
		template = [ ['X' for x in range(9)] for j in range(3) ] # Template without blanks with 'X' to be changed to numbers
		numbers0_8_original = list( range(9) )
		numbers0_8 = numbers0_8_original[::]

		# Fill first 2 rows with blanks randomly so that each of 8 coloumns has only 1 blank
		for row in range(2): 
			for k in range(4):
				template[row][ randomizer(numbers0_8) ] = '  '

		# Fill the last row with blanks randomly but the last 9th row obligatory
		last_number = numbers0_8[0] # last 9th coloumn without blanks
		numbers0_8 = numbers0_8_original[::]
		numbers0_8.remove(last_number)
		template[2][ last_number ] = '  ' # Fill last coloumn with blank
		for k in range(3): # Fill left 3 blanks
			template[2][ randomizer(numbers0_8) ] = '  '

		# Mix the rows betwean each other so blanks in all cards don't look the same
		mixed_template = []
		numbers0_2 = [0,1,2]
		for j in range(3):
			mixed_template.append( template[ randomizer(numbers0_2) ] )

		# SET VALUES
		card = mixed_template
		# Create list of lists with all possible numbers. Each list containes numbers for correspondent coloumn in card
		numbers_for_cards = []
		for y in range(9):
			numbers_for_cards.append( list( range( y*10, (y+1)*10 ) ) )
		numbers_for_cards[0].remove(0)
		numbers_for_cards[-1].append(90)

		# Fill 'X's with numbers
		for caloumn in range(9):
			# Each iteration put 2 random numbers in row_numbers list from a correspondent list in numbers_for_cards
			row_numbers = []
			row_numbers.append( randomizer( numbers_for_cards[caloumn] ) )
			row_numbers.append( randomizer( numbers_for_cards[caloumn] ) )
			row_numbers = sorted(row_numbers) # Sort row_numbers so we can put bigger numbers lower
			for row in range(3): # Fill the 'X's with numbers
				if card[row][caloumn] == 'X':
					card[row][caloumn] = row_numbers[0] # Since we have 3 positions in coloumn and 2 numbers to put we work only with first element of row_numbers
					row_numbers.pop(0)
		self.card = card

	def delete(self, number):
		'''
		Has one argument - number to be deleted. Returns flag which is False if number not in the card else True
		'''
		flag = False
		card = self.card
		for row in card:
			if number in row:
				number_index = row.index(number)
				row[number_index] = '  '
				flag = True
		return flag

	def numbers_left(self):
		'''
		Doesn't take arguments. Returns the number of numbers left in the card
		'''
		count = 0
		card = self.card
		for row in card:
			for element in row:
				if type(element) == int: count += 1
		return count

	def display(self):
		'''
		Doesn't take arguments. Displays the card so it looks like one
		'''
    	# Add spaces to the first coloumn because it has only one-digit numbers
		card = self.card
		if card[0][0] == '  ': card[0][0] = ' '
		if card[1][0] == '  ': card[1][0] = ' '
		if card[2][0] == '  ': card[2][0] = ' '

		# Convert numbers in card to string
		display_card = [[],[],[]]
		for j, row in enumerate(card):
			for number in row:
				display_card[j].append( str(number) )

		for j in range(3):
			print('-'*45)
			print( '| ' + ' | '.join( display_card[j] ) + ' |' )
		print('-'*45)

spaces = '\n'*50

# ENTER NUMBERS OF PLAYERS AND CARDS
# Give user take 3 shots to choose nu,ber of players and cards
for j in range(3):
	number_of_players = input('Enter number of players: ')
	if not ( number_of_players.isdigit() and int(number_of_players) > 0 ): # Check for correct input
		if j != 2: print('Pick your number') # Stop after 3rd try - not show Pick number string
		flag_1 = False
	else:
		number_of_players = int(number_of_players)
		flag_1 = True
		break
if not flag_1:
	input('I just assume you don\'t wanna play :(')
	exit()

for j in range(3):
	number_of_cards = input('Enter number of card: ')
	if not ( number_of_cards.isdigit() and int(number_of_cards) > 0 ): # Check for correct input
		if j != 2: print('Pick your number') # Stop after 3rd try - not show Pick number string
		flag_2 = False
	else:
		number_of_cards = int(number_of_cards)
		flag_2 = True
		break
if not flag_2:
	input('I just assume you don\'t wanna play :(')
	exit()

# ENTER PLAYERS NAMES AND PREPARE LISTS OF PLAYERS AND CARDS
player = []
for j in range(1, number_of_players + 1):
	name = input( 'Enter the name of player ' + str(j) + ': ' )
	if len(name) == 0: name = 'Player ' + str(j) # If name is not chosen - standart name is added
	player.append(name)
card = [ 'card ' + str(j) for j in range(1, number_of_cards + 1) ]

# GENERATE CARDS FOR ALL USERS
# Put cards in dictionarry of dictionarries
players = dict.fromkeys(player)
for p in range( len(players) ):
	players[ player[p] ] = dict.fromkeys(card)
	for c in range( len(players[ player[p] ]) ):
		players[ player[p] ][ card[c] ] = Loto()

# SHOW CARDS BEFORE START PLAYING
for p in range( len(player) ):
	for c in range( len(card) ):
		print( '\n' + ' '*46 + player[p] + ' ' + card[c] )
		players[ player[p] ][ card[c] ].display()

# PICK NUMBERS AND PLAY
all_numbers = Loto.all_numbers[::]
count = len(all_numbers)
for j in range( len(all_numbers) ):
	if count == 0 or len(player) == 0: print('The game is over'); exit()
	# Possibility to choose the picked number
	cheat = input('Press Enter to pick a number, ' + str(count) + ' left')
	if len(cheat) == 0:
		picked_number = all_numbers.pop(0)

	if cheat.isdigit():
		picked_number = int(cheat)
		all_numbers.remove(picked_number)

	# Skip the number of numbers untill certain number of numbers is left in a card
	if type(cheat) != int and cheat[:4] == 'skip':
		number_of_moves = int( cheat[ 5 : cheat.find('-') ] )
		number_of_left_numbers = int( cheat[ cheat.find('-')+1 : ] )
		stop = False
		for j in range(number_of_moves):
			picked_number = all_numbers.pop(0)
			count -= 1
			for p in range( len(players) ):
				for c in range( len( players[ player[p] ] ) ):
					current_card = players[ player[p] ][ card[c] ]
					current_card.delete(picked_number)
					if current_card.numbers_left() == number_of_left_numbers: stop = True
			if stop: break
		continue

	print( spaces + 'The number is ' + str(picked_number) )

	for p in range( len(player) ): # Delete won players
		if 0 in player: player.remove(0)

	for p in range( len(player) ):
		win_flag = False
		players_numbers = 0 # Variable for countimg players numbers to track who wins
		for c in range( len( players[ player[p] ] ) ):
			current_card = players[ player[p] ][ card[c] ]
			print( ' '*46 + player[p] + ' ' + card[c] )
			current_card.display()
			input()
			if current_card.delete(picked_number):
				print( '*'*46 + player[p] + ' ' + card[c] + ' has it! Numbers left -> ' + str(current_card.numbers_left()) + '\n')

			else:
				print( 'Nothing for ' + player[p] + ' ' + card[c] + '. Numbers left -> ' + str(current_card.numbers_left()) + '\n')

			players_numbers += current_card.numbers_left()

			if current_card.numbers_left() == 0: players[ player[p] ].pop( card[c] ) # Remove empty card

		if players_numbers == 0: # Print that player won
			print('\n'*3 + '*'*40 + player[p] + ' IS A WINNER ! ! !' + '*'*40 + '\n'*3)	
			player[p] = 0 # Marked player who won

	count -= 1
