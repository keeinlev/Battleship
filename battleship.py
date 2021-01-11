#KEVIN LEE
#BATTLESHIP GAME ASSIGNMENT
#ICS 3U
#MRS QUESNELLE
#DUE 13 NOVEMBER 2018


#functions and library imports
import random
import time
import math

def cls():
    print('\n'*80)
    
def grid():
    board = []
    numbers = []
    letters = []
    for i in range(dimension):
        letters.append(chr(65+i))
    for i in range(1, 1+dimension):
        numbers.append(str(i))
    print('  '+' '.join(numbers))
    for i in range(0, dimension * dimension):
        board.append("•")
    for i in range(0, len(board), dimension):
        print(letters[i//10] +' ' + " ".join(board[i:i+dimension]))

    return board

def guessGrid():
    numbers = []
    letters = []
    for i in range(dimension):
        letters.append(chr(65+i))
    for i in range(1, 1+dimension):
        numbers.append(str(i))
    print('  '+' '.join(numbers))
    for i in range(0, len(board), dimension):
        print(letters[i//10] +' ' + " ".join(board[i:i+dimension]))

def getBoardLocations(dimension):
    #This function will generate a dictionary of pairs
    #based on the SQUARE board dimension and 
    #location to list index on board
    #this can be used as a lookup for with index is meant by user index.
    #example. A1 = 0, B1 = 10, C1 = 10
    
    boardLocations = {}
    index = 0
    for row in range(0, dimension):
        for col in range(1, dimension+1):
            boardLocations[chr(row+65)+str(col)] = index
            index += 1
    
    return boardLocations




def generateRandomShips(dimension):
    #This function generates all the random ships you wish to place on a board

    allShips = []

    for shipLength in [5,4,3,3,2]:
        
        ship = getNewShipLocation(dimension, shipLength)
        while(overlapShips(ship, allShips) == True):
            ship = getNewShipLocation(dimension, shipLength)
        allShips.append(ship)

    return allShips

def getNewShipLocation(dimension, shipSize):
    #Function generates ONE new randomly placed ship on the board of given length

    #creates a list of all the indexes where ship is
    ship = []

    #limit the random placement for the ship within bounds of board
    row = random.randint(1, dimension - shipSize)
    col = random.randint(0, dimension - shipSize)
    direction = random.choice(["hor", "ver"])

    if direction == "hor":
        for i in range(0, shipSize):
            ship.append(dimension*(row-1) + col + i)

    else:
        for i in range(-1, shipSize-1):      
            ship.append(dimension*(row+i) + col)

    return ship

def overlapShips(newShip, allShips):
    #Function checks if a new ship has any overlapping spots with the already placed ships.
    for ship in allShips:
        if list(set(newShip) & set(ship)) != []:
            return True
            
    return False


def hitMiss(guess,real):
    #will change the character on the board related to the guess index to an 'x' for a hit or an 'o' for a miss
    for ship in real:
        if guess in ship:
            board[guess] = 'x'
            return 'Hit!'
        elif guess not in ship:
            continue
    board[guess] = 'o'
    return 'Miss!'

def count(guess,allShips):
    #returns a variable to identify which ship is being hit for purposes such as updating targets on a ship left, life bar, etc.
    for i in range(len(allShips)):
        if guess in allShips[i]:
            num = i
            return num

def lifeBar(names,oldLengths,newLengths):
    #makes a life bar of all ships using shipLengths storage list and allShips list
    hit = 'x'
    lives = 'o'
    for i in range(len(oldLengths)):
        print(f'{names[i]:>16} : {lives*newLengths[i]}{hit*(len(oldLengths[i])-newLengths[i])}') #string repetition and formatting

def getShipsLeft(lengths):
    #finds out how many ships haven't been completely hit
    left = 0
    for i in range(len(lengths)):
        if lengths[i] != 0:
            left += 1
    return left
        

def gameOver(turns,time):
    #lots of conditionals and extra grammar work for the ending congratulations
    adjective = ''
    article = ''
    if turns <= 17:
        adjective = 'PERFECT'
    elif turns >17 and turns < 25:
        adjective = 'ASTONISHING'
    elif turns >25 and turns < 35:
        adjective = 'EXCELLENT'
    elif turns >35 and turns < 50:
        adjective = 'DECENT'
    elif turns >50 and turns < 70:
        adjective = 'SLOW'
    elif turns >70:
        adjective = 'WHOPPING'
    if adjective[0] == 'a':
        article = 'an'
    else:
        article = 'a'
    print(f'\nCongratulations! You sunk all of the enemy\'s ships in {article} {adjective} {turns} turns with {time} minutes remaining!')       #gives user a rundown of their performance

def timeLeft(seconds):
    #use of a rounded time.process_time() value to subtract from initial seconds variable to calculate time left for the user
    if seconds//60 == 0 and seconds%60 < 10:
        return '00:0' + str(seconds%60)
    elif seconds%60<10:
        return str(seconds//60) + ':' + '0' + str(seconds%60)
    elif seconds//60 == 0:
        return '00:'+ str(seconds%60)
    else:
        return str(seconds//60) + ':' + str(seconds%60)
    
#MAIN

#INTRODUCTION
print(f'\n\n{"WELCOME TO BATTLESHIP":^80}\n\n{"*"*80}\n{"GOAL: THERE ARE SHIPS OF VARYING LENGTHS HIDDEN ON A GRID THAT ARE PLACED":^80}')
print(f'{"RANDOMLY. YOUR GOAL IS TO SINK THEM ALL BY GUESSING THEIR LOCATIONS AND":^80}')
print(f'{"FIRING MISSILES AT THEM. YOU WILL WIN ONCE ALL SHIPS ARE SUNK.":^80}\n\n')
print(f'{"YOU HAVE 4 MINUTES...GOOD LUCK!":^80}\n\n')
input(f'{"PLEASE PRESS ENTER TO BEGIN":^80}\n')
cls()

#a bunch of variables being defined
dimension = 10
board = grid()
shipCount = 0 
boardLocations = getBoardLocations(dimension)
allShips = generateRandomShips(dimension)
allShips2 = allShips
shipLengths = []
shipNames = ['Aircraft Carrier','Battleship','Destroyer', 'Submarine',  'Patrol Ship']
chars = ['A', 'B', 'D', 'S', 'P']
targets = 0
turns = 0
seconds = 240
guesses = []

#makes a second list for ship lengths to store for later and generates a number of targets
for i in range(len(allShips)):
    shipLengths.append(len(allShips[i]))
    targets+= shipLengths[i]


#where the fun begins
guess = input('\n'*6 + 'Please indicate where you would like shoot. Enter QUIT to exit.\n').upper()
timer = seconds
#basically all user inputs and function calls are in this while loop
while (targets != 0 and timer != 0 and guess != 'QUIT'):
    clock = math.ceil(time.process_time())             #this variable gets updated every time the user makes a move
    timer = seconds-clock                       #storage variable
    print(allShips)
    
    if guess not in boardLocations:           #error checking to prevent crashes
        guessGrid()
        print("Your input is invalid.\n")

    elif guess in guesses:           #error checking to prevent input of same guess
        guessGrid()
        print(f'You have already entered {guess}.\n')        

    else:
        guesses.append(guess)
        index = boardLocations[guess]
        s = hitMiss(index, allShips)
        guessGrid()
        print(f'\nThe spot {guess} was a {s}\n')
        turns += 1
        
        if s == 'Miss!':
            pass
            
        elif s == 'Hit!':
            targets = targets-1
            num = count(index,allShips)     #example of where 'count' function becomes useful
            shipLengths[num] -= 1
            
            if shipLengths[num] == 0:           #sees if there are no targets left on the ship that was just hit
                print(f'You sunk the enemy\'s {shipNames[num]}!\n')
                
            if targets != 0:
                pass
            
            elif targets == 0:
                break
            
        print(f'You have {targets} targets and {getShipsLeft(shipLengths)} ships left!')
        lifeBar(shipNames,allShips,shipLengths)
    print(f'\nYou have {timeLeft(timer)} seconds remaining\n')
    guess = input("\nPlease indicate where you would like shoot. Enter QUIT to exit.\n").upper()

cls()
if guess == 'QUIT':
    print('You gave up!')
elif timer == 0:
    print('You ran out of time!')
else:
    gameOver(turns,timeLeft(timer))

    
print('\nHere are the locations of the ships:\n')
for ship in range(len(allShips)):                   #reveals ship locations using ship characters A, B, S, D, P
    for i in allShips[ship]:
        board[i] = chars[ship]
guessGrid()


#GAME OVER!
