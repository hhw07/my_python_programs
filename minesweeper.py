b = """
Console Minesweeper.

':' will be initial console.
'newgame x y l' will start a new game of x by y with l mines.
'loadgame filename' will load saved game from JSON file.
'exit' or 'quit' will exit the game.
'help' will display this text

Enter commands to break and flag tiles.
'> ' will be for entering commands.
'flag x y' will flag the tile at coordinates x and y.
'break x y' will break the tile at coordinates x and y (and any other tiles it reveals.)
'quit' or 'exit' will exit game without saving.
'save filename' will save current game in JSON file.
'help' will display this text
"""

import json
import os
from random import randint
import time

clear_command = 'cls'

a = [-1, 0, 1]

def generate_mine(x, y):
	# Function to generate a random mine
	xc = randint(1, x) - 1
	yc = randint(1, y) - 1
	return [yc, xc]

def generate_minefield(x, y, l):
	# Uses generate_mine function to generate l mines in the x by y field.
	mines = []
	for i in range(l):
		while True:
			mine = generate_mine(x, y)
			if mine not in mines:
				mines.append(mine)
				break
	
	return mines

def generate_map_structure(x, y):
	# Generates Empty Map
	map = []
	for i in range(y):
		row = []
		for j in range(x):
			row.append([-2, False, False])
		map.append(row)

	return map

def find_value(x, y, mines):
	# Finds the number on the tile.
	v = 0

	for m in a:
		x += m
		for n in a:
			y += n
			if [y, x] in mines and x >= 0 and y >= 0:
				v += 1
			y -= n
		x -= m

	return v

def fill_map(clearmap, minefield):
	# Fills map with mines and numbers.
	x = len(clearmap)
	y = len(clearmap[0])
	for i in range(x):
		for j in range(y):
			if [j, i] in minefield:
				clearmap[i][j][0] = -1
				continue

			clearmap[i][j][0] = find_value(i, j, minefield)
	
	return clearmap

def printmap(mymap):
	print()
	x = len(mymap[0])

	colno = "     |"
	for i in range(x):
		colno += f"{i:^3}|"
	print(colno)
	print()

	rowline = "      "
	for i in range(x):
		rowline += "--- "
	print(rowline)

	for x in range(len(mymap)):
		i = mymap[x]
		row = f"{x:<3}  | "
		for j in i:
			if j[1] == True:
				if j[0] >= 0:
					row += str(j[0])
				else:
					row += "@"
			elif j[2] == True:
				row += "F"
			else:
				row += " "
			row += " | "
		row = row[:-1]
		print(row)
		print(rowline)
	print()

def breakgame(mymap):
	for j in mymap:
		for k in j:
			if k[0] == -1:
				k[1] = True
				time.sleep(0.25)
				os.system(clear_command)
				printmap(mymap)

def check_if_lost(mymap):
	lost = False
	for i in mymap:
		notlost = True
		for j in i:
			if j[0] == -1 and j[1] == True:
				notlost = False
				break
		if not notlost:
			lost = True
			break
	return lost

def check_if_won(mymap):
	won = True
	for i in mymap:
		notwon = False
		for j in i:
			if j[1] == False and j[0] != -1:
				notwon = True
				break
		if notwon:
			won = False
			break
	return won

def check_if_mines_covered(mymap, x, y, xlen, ylen):
	v = 0
	
	for m in a:
		x += m
		for n in a:
			y += n
			if 0 <= y < ylen and 0 <= x < xlen:
				if mymap[y][x][2]:
					v += 1
			y -= n
		x -= m
	
	if v == mymap[y][x][0]:
		return True
	return False

def breaktile(mymap, x, y, xlen, ylen):
	if not check_if_mines_covered(mymap, x, y, xlen, ylen):
		return
	for m in a:
		x += m
		for n in a:
			y += n
			if 0 <= y < ylen and 0 <= x < xlen:
				if not (mymap[y][x][2] or  mymap[y][x][1]):
					mymap[y][x][1] = True
					if mymap[y][x][0] == 0:
						breaktile(mymap, x, y, xlen, ylen)
			y -= n
		x -= m

def find_flags_mines(mymap):
	mines = 0
	flags = 0
	for i in mymap:
		for j in i:
			if j[0] == -1:
				mines += 1
			if j[2] == True:
				flags += 1
	return [flags, mines]

def init_console(a):
	os.system(clear_command)
	while True:
		command = input(": ").lower().split()
		if command[0] == "newgame":
			x = int(command[1])
			y = int(command[2])
			l = int(command[3])

			thismap = generate_map_structure(x, y)
			mymines = generate_minefield(x, y, l)

			thismap = fill_map(thismap, mymines)
			game_console(thismap, l)
			os.system(clear_command)

		elif command[0] == "loadgame":
			filename = command[1] + ".json"
			with open(filename, 'r') as myfile:
				thismap = json.load(myfile)

			a = find_flags_mines(thismap)
			flags = a[0]
			mines = a[1]
			del a

			game_console(thismap, mines, flagged=flags)
			os.system(clear_command)

		elif command[0] == "quit" or command[0] == "exit":
			os.system(clear_command)
			break
		elif command[0] == "help":
			print(a)

def game_console(mymap, l, flagged=0):
	os.system(clear_command)
	ylen = len(mymap)
	xlen = len(mymap[0])

	while True:
		printmap(mymap)
		print(f"Flags remaining: {l - flagged}")

		command = input("> ").lower().split()
		if command[0] == "flag":
			y = int(command[2])
			x = int(command[1])
			if 0 <= y < ylen and 0 <= x <= xlen:
				if mymap[y][x][1] == False:
					mymap[y][x][2] = not mymap[y][x][2]
					if mymap[y][x][2]:
						flagged += 1
					else:
						flagged -= 1
				else:
					print("This tile is already broken.")
					time.sleep(2)
					os.system(clear_command)
					continue
		elif command[0] == "break":
			y = int(command[2])
			x = int(command[1])
			if 0 <= y < ylen and 0 <= x <= xlen:
				if (not mymap[y][x][2]) and 0 <= y < ylen and 0 <= x <= xlen:
					if mymap[y][x][1] or mymap[y][x][0] == 0:
						breaktile(mymap, x, y, xlen, ylen)
					mymap[y][x][1] = True
					if check_if_lost(mymap):
						breakgame(mymap)
						os.system(clear_command)
						printmap(mymap)
						print("\nGame over.")
						print("Press Enter to exit.")
						s = input("")
						break
				if check_if_won(mymap):
					os.system(clear_command)
					printmap(mymap)
					print("\nYou won!\nCongratulations!")
					break
		elif command[0] == "quit" or command[0] == "exit":
			q = input("Quit without saving?[y/n]: ")
			if q.lower() == "y":
				break
			else:
				print("Enter 'save filename' to save in JSON file.")
				time.sleep(3)
		elif command[0] == "save":
			with open(command[1] + ".json", 'w') as myfile:
				json.dump(mymap, myfile)
			print("Saved current game progress in " + command[1] + ".json")
			time.sleep(3)
		elif command[0] == "help":
			print(a)
		os.system(clear_command)

init_console(b)