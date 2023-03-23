# words = ["hulk", "currant", "complex", "create", "thing", "skewer", "cloud", "diamond", "spartan"]

# words = ["cartography", "artemis", "blemish", "cloud", "doom"]

words = ["spanish", "index", "aeroplane", "boston", "signal", "board", "hair", "token", "load", "golf"]

class C:
    horizontal = True
    vertical = False
    blank = " "

class wordInfo():
    def __init__(self, word, x, y, v):
        self.word = word
        self.x = x
        self.y = y
        self.v = v

def len_chars(words):
    l = 0
    for i in words:
        l += len(i)
    return l

def create_matrix(x, y):
    matrix = [None]
    for i in range(y):
        a = []
        for j in range(x):
            a.append(C.blank)
        matrix.append(a)
    return matrix

def display_matrix(matrix):
    for i in range(len(matrix)-1):
        a = "    "
        for j in matrix[i+1]:
            a += j
            a += " "
        print(a)

def add_word(matrix, wordinfo):
    word = wordinfo.word
    x = wordinfo.x
    y = wordinfo.y
    v = wordinfo.v
    if v == C.horizontal:
        for i in range(len(word)):
            matrix[y][x+i] = word[i]
    elif v == C.vertical:
        for i in range(len(word)):
            matrix[y+i][x] = word[i]

def remove_word(matrix, wordinfo):
    word = wordinfo.word
    x = wordinfo.x
    y = wordinfo.y
    v = wordinfo.v
    if v == C.horizontal:
        for i in range(len(word)):
            if matrix[y+1][x+i] == C.blank and matrix[y-1][x+i] == C.blank:
                matrix[y][x+i] = C.blank
    elif v == C.vertical:
        for i in range(len(word)):
            if matrix[y+i][x+1] == C.blank and matrix[y+i][x-1] == C.blank:
                matrix[y+i][x] = C.blank

def check1(wordinfo, word):
    L = []
    for i in range(len(wordinfo.word)):
        for j in range(len(word)):
            if wordinfo.word[i] == word[j]:
                L.append([i, j])

    return L

def check2(matrix, wordinfo):
    check = True
    word = wordinfo.word
    x = wordinfo.x
    y = wordinfo.y
    a = " "
    # print(word, " - ", x, y)
    if wordinfo.v == C.horizontal:
        if matrix[y][x-1] != C.blank or matrix[y][x+len(word)] != C.blank:
            # print(word, x, y, -1)
            # print(word, "-end")
            return False

        for i in range(len(word)):
            if matrix[y][x+i] == C.blank and matrix[y-1][x+i] == C.blank and matrix[y+1][x+i] == C.blank:
                # print(word, "-noxtion")
                continue
            else:
                if matrix[y][x+i] == word[i]:
                    # print(word, "-xtion")
                    continue
                else:
                    # print(word, x+i, y, i)
                    # print(word, "-break")
                    check = False
                    break
    elif wordinfo.v == C.vertical:
        if matrix[y-1][x] != C.blank or matrix[y+len(word)][x] != C.blank:
            # print(word, x, y, -1)
            # print(word, "-end")
            return False

        for i in range(len(word)):
            if matrix[y+i][x] == C.blank and matrix[y+i][x-1] == C.blank and matrix[y+i][x+1] == C.blank:
                # print(word, "-noxtion")
                continue
            else:
                if matrix[y+i][x] == word[i]:
                    # print(word, "-xtion")
                    continue
                else:
                    # print(word, x, y+i, i)
                    # print(word, "-break")
                    check = False
                    break

    return check

def createCrossword(words, crossword=None, wordinfo=None, initword=None):
    if len(words) == 0:
        return crossword
    a = words[-1]

    # Initialise
    if crossword == None:
        l = len_chars(words)
        L = 2*l + 1
        crossword = create_matrix(L, L)
        words.remove(a)
        aInfo = wordInfo(a, l, l, C.horizontal)
        add_word(crossword, aInfo)
        wordinfo = [aInfo]
        crossword = createCrossword(words, crossword, wordinfo)

    else:
        w = wordinfo[-1]
        pts = check1(w, a)

        checked = False

        for i in pts:
            # print(a, i)
            if w.v == C.horizontal:
                testword = wordInfo(a, w.x+i[0], w.y-i[1], C.vertical)
            elif w.v == C.vertical:
                testword = wordInfo(a, w.x-i[1], w.y+i[0], C.horizontal)

            # print(testword.word, i[0], i[1], check2(crossword, testword), testword.x, testword.y, testword.v)
            
            if check2(crossword, testword):
                checked = True
                crossword[0] = checked
                # print(testword.word)

                words.remove(a)
                wordinfo.append(testword)
                add_word(crossword, testword)

                # print(crossword[0])
                crossword = createCrossword(words, crossword, wordinfo)
                # display_matrix(crossword)
                # print("\n")

                checked = crossword[0]
                # print(checked)
                if checked:
                    break
                else:
                    # print("Hello there.")
                    # display_matrix(crossword)
                    # print("General Kenobi.\n")
                    words.append(a)
                    wordinfo.remove(testword)
                    remove_word(crossword, testword)

        if not checked:
            # print(a, words, initword)
            if initword == a:
                return crossword
            if initword == None:
                initword = a
            words.remove(a)
            words = [a] + words
            crossword = createCrossword(words, crossword, wordinfo, initword)
            # display_matrix(crossword)

        crossword[0] = True

        # crossword[0] = checked
        # print("HEY")

    return crossword

def trim(matrix):
    x, y = len(matrix[0]), len(matrix)
    minx, miny = x, y
    maxx, maxy = 0, 0
    for i in range(x):
        for j in range(y):
            if matrix[j][i] != C.blank:
                if i < minx:
                    minx = i
                if i > maxx:
                    maxx = i
                if j < miny:
                    miny = j
                if j > maxy:
                    maxy = j

    matrix = matrix[miny:maxy+1]
    newmatrix = []
    for i in matrix:
        newmatrix.append(i[minx:maxx+1])

    return newmatrix


test = createCrossword(words)
test = test[1:]
test = trim(test)
test = [True] + test
print("\n")
display_matrix(test)
print("\n")