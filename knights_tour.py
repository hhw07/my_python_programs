# Knight's Tour solution
illegal_moves = [-1, -2, 8, 9]
max_pos = [0]

def move(positions):
	if len(positions) == 64:
		return positions

	n = len(positions)

	x = positions[-1][0]
	y = positions[-1][1]

	possible_moves = [[x+2, y+1], [x+1, y+2], [x-1, y+2], [x-2, y+1], [x-2, y-1], [x-1, y-2], [x+1, y-2], [x+2, y-1]]

	for i in possible_moves:
		if (i not in positions) and (i[0] not in illegal_moves) and (i[1] not in illegal_moves):
			positions.append(i)
			positions = move(positions)

			if len(positions) < 64:
				while len(positions) > n:
					del positions[-1]
			else:
				break

	return positions

def drawboard(board):
	myboard = [[0 for i in range(8)] for j in range(8)]
	for k in range(64):
		y = board[k]
		myboard[y[0]][y[1]] = k+1
	
	return myboard

a = move([[0, 0]])
aboard = drawboard(a)
for i in aboard:
	print("%4d%4d%4d%4d%4d%4d%4d%4d"%(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]))
