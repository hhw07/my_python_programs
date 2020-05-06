# 8 Queens Problem

def diagonal_check(positions, p):
	n = len(positions)
	check = False

	for i in range(n):
		Δx = n - i
		Δy = p - positions[i]

		if (Δx == Δy) or (Δx == -Δy):
			check = True
			break
	return check

def find_pos(found):
	# found_pos contains list of all possible 8-queen arrangements
	found_pos = []

	if len(found) == 7:
		final = True
	else:
		final = False

	for i in range(8):
		if not (diagonal_check(found, i) or (i in found)):
			found.append(i)

			if final:
				found_pos.append(found[:])
			else:
				for j in find_pos(found):
					found_pos.append(j)

			del found[-1]
	return found_pos

def drawboard(board):
	myboard = [[" - |" for i in range(8)] for j in range(8)]
	for i in range(8):
		myboard[i][board[i]] = " Q |"
	
	for i in range(8):
		n = ""
		for j in myboard[i]:
			n += j
		myboard[i] = n

	return myboard

a = find_pos([])
for x in range(len(a)):
	print("Solution %d" %x)
	for i in drawboard(a[x]):
		print(i)
	print("\n")
