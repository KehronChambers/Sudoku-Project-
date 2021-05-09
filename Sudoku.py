#pyhon file to help solve sudoku
#used https://techwithtim.net/tutorials/python-programming/sudoku-solver-backtracking/ as a guideline to help construct program

def findEmptyBox(box):#empty square in the boardd
    for a in range(len(box)):#loops through board
        for b in range(len(box[a])):#length of each row##
            if box[a][b] == 0:#checks if position is 0
                return (a, b)  # row, col

def solver(box):#uses recurrsion 
    search = findEmptyBox(box)
    if not search:
        return True#solution is found and board is full
    else:
        row, col = search#else user can keep inputting values into board

    for a in range(1,10):#loops through values that are being used for solution
        if valid(box, a, (row, col)):#if valid
            box[row][col] = a#input is placed in board

            if solver(box):
                return True#sub is constantly called until finished

            box[row][col] = 0#if valid is incorrect we backtrack and reset the value and repeat process

    return False#if input is invalid 


def valid(box, num, pos):#checks to see if the current board is valid
    for a in range(len(box[0])):#loops through each column in the row
        if box[pos[0]][a] == num and pos[1] != a:
            return False#if entered number is repeated return false


    for a in range(len(box)):#loops through each row in column
        if box[a][pos[1]] == num and pos[0] != a:
            return False#if entered number is repeated return false

    # Checking box using integer position
    row_boxes = pos[1] // 3#integer divide row
    column_boxes = pos[0] // 3#integer divide column 

    for a in range(column_boxes*3, column_boxes*3 + 3):#loop through all nine elements in box 
        for b in range(row_boxes * 3, row_boxes*3 + 3):#look through the values in each grid
            if box[a][b] == num and (a,b) != pos:#check if repeated numbers are in box
                return False#returns false if duplicate is found

    return True#if checks are passed then true is returned


    return None#no blank squares means we're done
