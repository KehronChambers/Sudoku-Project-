#visual representation of the game in pygame
#pygame gui retrieved from https://techwithtim.net/tutorials/python-programming/sudoku-solver-backtracking/
import pygame
from Sudoku import solver, valid#importing code file into gui file and other values
import time
pygame.font.init()


class Grid:#grid class
    #grid of values that start on board 
    #to change starting board use this grid 
    board = [
        [4, 2, 0, 1, 7, 0, 3, 9, 0],
        [0, 7, 8, 0, 0, 0, 0, 5, 0],
        [0, 0, 0, 8, 0, 0, 2, 0, 7],
        [0, 5, 0, 0, 0, 7, 0, 3, 0],
        [3, 0, 0, 2, 9, 6, 0, 0, 5],
        [0, 1, 0, 5, 0, 0, 0, 7, 0],
        [7, 0, 1, 0, 0, 8, 0, 0, 0],
        [0, 6, 0, 0, 0, 0, 9, 4, 0],
        [0, 9, 3, 0, 2, 4, 0, 8, 1]
    ]

    def __init__(self, rows, cols, width, height):#attributes
        self.rows = rows#rows
        self.cols = cols#columns
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]#cube
        self.width = width#width
        self.height = height#height
        self.model = None#model
        self.selected = None#selected


    def update_model(self):#board sent to solver to see if board can be solvable and has final values
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):#sets permanent value
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()#if value of box is 0 then update to inputted value

            if valid(self.model, val, (row,col)) and solver(self.model):
                return True#if inputted value is same as model value then return true
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False#if else then return false and answer is wrong

    def sketch(self, val):#set temp value
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self, win):
        #draws grid lines
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        #draws cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)

    def select(self, row, col):#select desired square
        #reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):#lets you remove a temp entered number
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):#return position on cube clicked on
        """
        :param: pos
        :return: (row, col)
        """
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None

    def is_finished(self):#checks if no empty squares on board
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True


class Cube:#cube class
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width ,height):
        self.value = value#set value inputted
        self.temp = 0#tempoary value
        self.row = row#row
        self.col = col#column
        self.width = width#width
        self.height = height#height
        self.selected = False#selected set as false

    def draw(self, win):#drawing values
        fnt = pygame.font.SysFont("comicsans", 40)#font of values

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap#sets the gap between the values

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128,128,128))
            win.blit(text, (x+5, y+5))#will show temp value in box
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))#if value already there nothing will come up
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(win, (255,0,0), (x,y, gap ,gap), 3)#draws value in

    def set(self, val):
        self.value = val#sets value

    def set_temp(self, val):
        self.temp = val#sets temp value


def redraw_window(win, board, time, strikes):
    win.fill((255,255,255))
    # Draw time
    fnt = pygame.font.SysFont("comicsans", 40)
    text = fnt.render("Time: " + format_time(time), 1, (0,0,0))
    win.blit(text, (540 - 160, 560))
    # Draw Strikes
    text = fnt.render("X " * strikes, 1, (255, 0, 0))
    win.blit(text, (20, 560))
    # Draw grid and board
    board.draw(win)


def format_time(secs):#allows user to see how long he has spent
    sec = secs%60
    minute = secs//60
    hour = minute//60

    mat = " " + str(minute) + ":" + str(sec)
    return mat


def main():#main
    win = pygame.display.set_mode((540,600))#window size
    pygame.display.set_caption("Sudoku")#name of window
    board = Grid(9, 9, 540, 540)#board dimensions
    key = None#key starts with no value
    run = True#when program starts run is set to true
    start = time.time()#timer begins
    strikes = 0#incorrect answers are counted
    while run:

        play_time = round(time.time() - start)#shows playtime

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False#if user quits program is closed and run is set to false
            if event.type == pygame.KEYDOWN:#depending on what key is pressed is what will be displayed in program
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()#delete will clear entry
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = board.selected#confirm entered value
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")#if temp value is correct it will be permanent and this is displayed
                        else:
                            print("Wrong")
                            strikes += 1#if temp value is incorrect wrong is printed and a strike value is incrimented
                        key = None#after a key value is entered and submitted it returns back to 0 waiting for new value

                        if board.is_finished():
                            print("Game over")
                            print(play_time)
                            run = False#when game is finished game over is printed and program closes

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None#if u click a box its highlighted

        if board.selected and key != None:
            board.sketch(key)#if u click a box with a value already inside of it

        redraw_window(win, board, play_time, strikes)
        pygame.display.update()


main()
pygame.quit()
