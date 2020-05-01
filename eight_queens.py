# 8 Queens Problem
'''
[x0, x1, x2, x3, x4, x5, x6, x7]
'''

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

a = find_pos([])
for x in a:
	print(x)
