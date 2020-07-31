# tic tac toe 
import numpy as np
import random as rand


def init_board():
    print "Initialing Board"
    return np.array([[9, 9, 9], [9, 9, 9], [9, 9, 9]])


# check the heuristics of the new move thats made
def check_heuristic():
    print("\nChecking...\n")


# coin flip
def cf():
    num = rand.randint(0, 1);
    if num == 0:
        turn = 'A'
        User_turn()
    else:
        AI_turn()
        turn = 'B'
    return turn


# Set position at center of board
def AI_turn():
    print("Let's play")
    x = 1
    y = 1
    print(x, y)
    board[x][y] = 1
    coor_arr.append(tuple([x, y]))


# Ask User for their input every time
def User_turn():
    print("User's turn\n")
    x = input("Enter X - coordinate\n")
    y = input("Enter Y - coordinate\n")

    # check for valid coordinates
    while x >= 3 and y >= 3:
        x = input("Enter correct X - coordinate\n")
        y = input("Enter correct Y - coordinate\n")

    board[x][y] = 0
    coor_arr.append(tuple([x, y]))


def AI_turn2():
    print("New Moves\n")
    # check heuristics, greedy heuristics


def printBoard():
    for i in board:
        print i


# main method
coor_arr = []
board = init_board()
printBoard()
X = 'x'
Y = 'y'
turn = cf()
printBoard()

draw = False

# User's Turn
if turn is 'A':
    print("-----AI's Turn Now-----\n")
    while not draw:
        AI_turn2()
        printBoard()
        check_heuristic()
        if draw:
            break

        User_turn()
        printBoard()
        check_heuristic()
        if draw:
            break
        draw = True
else:  # AI's turn
    print("-----User's Turn Now-----\n")
    while not draw:
        User_turn()
        printBoard()
        check_heuristic()
        if draw:
            break

        AI_turn2()
        printBoard()
        check_heuristic()
        if draw:
            break
        draw = True

print "Printing coords used in this game...\n"
for t in coor_arr:
    print t
