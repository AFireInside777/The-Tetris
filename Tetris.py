import pygame, sys
from pygame.locals import *
import time
import random

pygame.init()

white = (255, 255, 255)
tetdisplay = pygame.display.set_mode((475, 640))
tetdisplay.fill(white)

#--Colors--#
black = (0, 0, 0)
white = (255, 255, 255)
red   = (255, 0, 0)
blue = (0,0,255)
green = (0,255,0)
orange = (255,165,0)
purple = (108, 0, 194)
score = 0

def TitleScreen(TetScreen):
    TetScreen.fill(white)
    font = pygame.font.SysFont(None, 35)
    img = font.render("Tetris", True, green)
    TetScreen.blit(img, (190, 100))
    pygame.display.update()
    
    img2 = font.render("Press Enter/Return to Start", True, green)
    TetScreen.blit(img2, (75, 320))
    pygame.display.update()

    pygame.event.clear()
    
    while True:
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                TetScreen.fill(white)
                break
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
TitleScreen(tetdisplay)

font = pygame.font.SysFont(None, 30)
img = font.render("Next Shape", True, green)
tetdisplay.blit(img, (343, 50))
pygame.display.update()

pygame.draw.rect(tetdisplay, black, (343, 98, 110, 110))
pygame.display.update()

font = pygame.font.SysFont(None, 30)
img = font.render("Score", True, green)
tetdisplay.blit(img, (367, 285))
pygame.display.update()

pygame.draw.rect(tetdisplay, black, (335, 322, 125, 75))
pygame.display.update()

font = pygame.font.SysFont(None, 60)
img = font.render(str(score), True, blue)
tetdisplay.blit(img, (348, 338))
pygame.display.update()

shapenames = ("cubeshape", "sshape", "tshape", "straightlineshape", "lshape")

lineofblocks = []
grid = []
currentshape = []
tetrisshapeinfo = []
perspectiveshape = []
ground = []
x = 0
y = 0

for row in range(20): ####################
    for column in range(10):
        lineofblocks.append ((pygame.draw.rect(tetdisplay, red, (y, x, 32, 32)), red)) # (rect(y, x, 32, 32), (255, 0, 0))
        y = y + 32
    grid.append(lineofblocks) # grid is made, array of rects with color
    lineofblocks = []
    y = 0
    x = x + 32
pygame.display.update()## For loop which draws rect in to first list, then adds list to grid list

def draw(shapecoords, color):
    for y, x in shapecoords:
        yc = grid[y][x][0][0] # ((y, x, 32, 32), (255, 0, 0)) = y = yc
        xc = grid[y][x][0][1] # ((y, x, 32, 32), (255, 0, 0)) = x = xc
        grid[y][x] = ((pygame.draw.rect(tetdisplay, color, (yc, xc, 32, 32)), color))
    pygame.display.update()
    
def drawmodel(modelcoords, color):
    pygame.draw.rect(tetdisplay, black, (343, 100, 110, 110))
    pygame.display.update()
    for yf, xf in modelcoords:
        pygame.draw.rect(tetdisplay, color, (yf, xf, 20, 20))

BlockModelLibrary = {
    "sshape" : [[(368, 150), (388, 130), (388, 150), (408, 130)], blue],
    "straightlineshape" : [[(388, 115), (388, 135), (388, 155), (388, 175)], purple],
    "cubeshape" : [[(377, 135), (397, 135), (377, 155), (397, 155)], green],
    "tshape" : [[(368, 135), (388, 135), (408, 135), (388, 155)], orange],
    "lshape" : [[(380, 122), (380, 142), (380, 162), (400, 162)], white]
    }

class NextShape():
    def __init__(self, model):
        self.model = model[0]
        self.modelcolor = model[1]
        drawmodel(self.model, self.modelcolor)

class TetrisBlock():
    
    global ground
        
    def __init__(self, coordinates):
        self.coordinates = coordinates[0]
        self.origcoords = coordinates[0]
        self.color = coordinates[1]
        draw(self.coordinates, self.color)
        
    def rotate(self, indicator): 
        
        if self.color == blue: ##################SSHAPE####################################################################
        
            rotatecoords = []
            if indicator == 0:
                
                rotatecoords.append((self.coordinates[1][0]-1, self.coordinates[1][1]-1))
                if rotatecoords[0][0] > -1:
                
                    draw(self.coordinates, red)     
                    
                    self.coordinates[1] = (self.coordinates[1][0]-1, self.coordinates[1][1]-1)
                    self.coordinates[2] = (self.coordinates[2][0]-1, self.coordinates[2][1]+2)
                    self.coordinates[3] = (self.coordinates[3][0], self.coordinates[3][1]+1)
                                
                    draw(self.coordinates, self.color)
                    
                    return 1
                
                else:
                    return 0
          
            if indicator == 1:
                
                rotatecoords.append((self.coordinates[1][0]+1, self.coordinates[1][1]+1))
                rotatecoords.append((self.coordinates[2][0]+1, self.coordinates[2][1]-2))
                rotatecoords.append((self.coordinates[3][0], self.coordinates[3][1]-1))
                
                if rotatecoords[0] not in ground and rotatecoords[1] not in ground and rotatecoords[2] not in ground:
                
                    draw(self.coordinates, red)
                        
                    self.coordinates[1] = (self.coordinates[1][0]+1, self.coordinates[1][1]+1)
                    self.coordinates[2] = (self.coordinates[2][0]+1, self.coordinates[2][1]-2)
                    self.coordinates[3] = (self.coordinates[3][0], self.coordinates[3][1]-1)
                    
                    if self.coordinates[2][1] < 0:
                        self.coordinates = [(y,x+1) for y,x in self.coordinates]
                        draw(self.coordinates, self.color)
                        return 0
                
                    else:
                        draw(self.coordinates, self.color)
                        return 0
                
                else:
                    return 1
                
        if self.color == orange: ###############TSHAPE#############################################################################
            
            rotatecoords = []
            
            if indicator == 0:
                
                rotatecoords.append((self.coordinates[0][0]-1, self.coordinates[0][1]+1))
                if rotatecoords[0][0] > -1:
                    draw(self.coordinates, red)      
                    self.coordinates[0] = (self.coordinates[0][0]-1, self.coordinates[0][1]+1)
                    draw(self.coordinates, self.color)
                    
                    return 1
                
                else:
                    return 0
          
            if indicator == 1:
                rotatecoords.append((self.coordinates[3][0]-1, self.coordinates[3][1]-1))
                if rotatecoords[0] not in ground:
                    draw(self.coordinates, red)
                    self.coordinates[3] = (self.coordinates[3][0]-1, self.coordinates[3][1]-1)
                    if self.coordinates[3][1] < 0:
                        self.coordinates = [(y,x+1) for y,x in self.coordinates]
                        draw(self.coordinates, self.color)
                        return 2
                
                    else:
                        draw(self.coordinates, self.color)
                        return 2
                    
            if indicator == 2:
                
                rotatecoords.append((self.coordinates[2][0]+1, self.coordinates[2][1]-1))
                
                if rotatecoords[0] not in ground:
                    
                    draw(self.coordinates, red)
                    
                    self.coordinates[2] = (self.coordinates[2][0]+1, self.coordinates[2][1]-1)
                    
                    if self.coordinates[3][1] < 0:
                        forloop = 0
                        for y, x in self.coordinates:
                            self.coordinates[forloop] = (y,x+1)
                            forloop = forloop + 1
                    
                        draw(self.coordinates, self.color)
                            
                        return 3
                
                    else:
                        draw(self.coordinates, self.color)
                        
                        return 3
                
            if indicator == 3:
                
                rotatecoords.append((self.coordinates[0][0]+1, self.coordinates[0][1]-1))
                rotatecoords.append((self.coordinates[2][0]-1, self.coordinates[2][1]+1))
                rotatecoords.append((self.coordinates[3][0]+1, self.coordinates[3][1]+1))
                
                if rotatecoords[0] not in ground and rotatecoords[1] not in ground and rotatecoords[2] not in ground:
                    
                    draw(self.coordinates, red)
                    
                    self.coordinates[0] = (self.coordinates[0][0]+1, self.coordinates[0][1]-1)
                    self.coordinates[2] = (self.coordinates[2][0]-1, self.coordinates[2][1]+1)
                    self.coordinates[3] = (self.coordinates[3][0]+1, self.coordinates[3][1]+1)
                
                    if self.coordinates[2][1] > 9:
                        forloop = 0
                        for y, x in self.coordinates:
                            self.coordinates[forloop] = (y,x-1)
                            forloop = forloop + 1
                
                        draw(self.coordinates, self.color)
                        
                    return 0
            
                else:
                    draw(self.coordinates, self.color)
                    
                    return 0
                
        if self.color == purple: ###############STRAIGHTLINE###################################
            
            rotatecoords = []
            
            if indicator == 0:
                
                rotatecoords.append((self.coordinates[0][0]+1, self.coordinates[0][1]-1))
                rotatecoords.append((self.coordinates[2][0]-1, self.coordinates[2][1]+1))
                rotatecoords.append((self.coordinates[3][0]-2, self.coordinates[3][1]+2))
                
                if rotatecoords[0] not in ground and rotatecoords[1] not in ground and rotatecoords[2] not in ground:
                
                    draw(self.coordinates, red)      
                    
                    self.coordinates[0] = (self.coordinates[0][0]+1, self.coordinates[0][1]-1)
                    self.coordinates[2] = (self.coordinates[2][0]-1, self.coordinates[2][1]+1)
                    self.coordinates[3] = (self.coordinates[3][0]-2, self.coordinates[3][1]+2)
                    
                    if self.coordinates[2][1] > 9 and self.coordinates[3][1] > 9:
                        self.coordinates = [(y,x-2) for y,x in self.coordinates]
                        draw(self.coordinates, self.color)
                        return 1
                    
                    elif self.coordinates[3][1] > 9:
                        self.coordinates = [(y,x-1) for y,x in self.coordinates]
                        draw(self.coordinates, self.color)
                        return 1
                    
                    elif self.coordinates[0][1] < 0:
                        self.coordinates = [(y,x+1) for y,x in self.coordinates]
                        draw(self.coordinates, self.color)
                        return 1
                
                    else:
                        draw(self.coordinates, self.color)
                        
                        return 1
          
            if indicator == 1:
                
                rotatecoords.append((self.coordinates[0][0]-1, self.coordinates[0][1]+1))
                rotatecoords.append((self.coordinates[2][0]+1, self.coordinates[2][1]-1))
                rotatecoords.append((self.coordinates[3][0]+2, self.coordinates[3][1]-2))
                
                if rotatecoords[0] not in ground and rotatecoords[1] not in ground and rotatecoords[2] not in ground:
                
                    draw(self.coordinates, red)
                        
                    self.coordinates[0] = (self.coordinates[0][0]-1, self.coordinates[0][1]+1)
                    self.coordinates[2] = (self.coordinates[2][0]+1, self.coordinates[2][1]-1)
                    self.coordinates[3] = (self.coordinates[3][0]+2, self.coordinates[3][1]-2)
                    
                    draw(self.coordinates, self.color)
                        
                    return 0
       
        if self.color == white: ##################LSHAPE####################################################################
        
            rotatecoords = []

            if indicator == 0:
                
                rotatecoords.append((self.coordinates[0][0]+2, self.coordinates[0][1]-2))
                rotatecoords.append((self.coordinates[1][0]+1, self.coordinates[1][1]-1))
                rotatecoords.append((self.coordinates[3][0]-1, self.coordinates[3][1]-1))

                if rotatecoords[0] not in ground and rotatecoords[1] not in ground and rotatecoords[2] not in ground:
                
                    draw(self.coordinates, red)      
                    
                    self.coordinates[0] = (self.coordinates[0][0]+2, self.coordinates[0][1]-2)
                    self.coordinates[1] = (self.coordinates[1][0]+1, self.coordinates[1][1]-1)
                    self.coordinates[3] = (self.coordinates[3][0]-1, self.coordinates[3][1]-1)

                    if self.coordinates[0][1] < 0 and self.coordinates[1][1] < 0:
                        self.coordinates = [(y,x+2) for y,x in self.coordinates]
                        draw(self.coordinates, self.color)                        
                        return 1
                    
                    elif self.coordinates[0][1] < 0:
                        self.coordinates = [(y,x+1) for y,x in self.coordinates]
                        draw(self.coordinates, self.color)
                        return 1
                    
                    else:
                        draw(self.coordinates, self.color)
                        return 1
          
            if indicator == 1:
                
                rotatecoords.append((self.coordinates[0][0]+2, self.coordinates[0][1]+2))
                rotatecoords.append((self.coordinates[1][0]+1, self.coordinates[1][1]+1))
                rotatecoords.append((self.coordinates[3][0]+1, self.coordinates[3][1]-1))
                
                if rotatecoords[0] not in ground and rotatecoords[1] not in ground and rotatecoords[2] not in ground:
                
                    draw(self.coordinates, red)
                        
                    self.coordinates[0] = (self.coordinates[0][0]+2, self.coordinates[0][1]+2)
                    self.coordinates[1] = (self.coordinates[1][0]+1, self.coordinates[1][1]+1)
                    self.coordinates[3] = (self.coordinates[3][0]+1, self.coordinates[3][1]-1)
                    
                    draw(self.coordinates, self.color)
                        
                    return 2
                
            if indicator == 2:
                
                rotatecoords.append((self.coordinates[0][0]-2, self.coordinates[0][1]+2))
                rotatecoords.append((self.coordinates[1][0]-1, self.coordinates[1][1]+1))
                rotatecoords.append((self.coordinates[3][0]+1, self.coordinates[3][1]+1))
                
                if rotatecoords[0] not in ground and rotatecoords[1] not in ground and rotatecoords[2] not in ground:
                
                    draw(self.coordinates, red)
                    
                    self.coordinates[0] = (self.coordinates[0][0]-2, self.coordinates[0][1]+2)
                    self.coordinates[1] = (self.coordinates[1][0]-1, self.coordinates[1][1]+1)
                    self.coordinates[3] = (self.coordinates[3][0]+1, self.coordinates[3][1]+1)
                    
                    if self.coordinates[0][1] > 9 and self.coordinates[1][1] > 9:
                        self.coordinates = [(y,x-2) for y,x in self.coordinates]
                        draw(self.coordinates, self.color)                        
                        return 3
                        
                    elif self.coordinates[0][1] > 9:
                        self.coordinates = [(y,x-1) for y,x in self.coordinates]                            
                        draw(self.coordinates, self.color)                        
                        return 3
                    
                    else:
                        draw(self.coordinates, self.color)                        
                        return 3
            
            if indicator == 3:
                
                rotatecoords.append((self.coordinates[0][0]-2, self.coordinates[0][1]-2))
                rotatecoords.append((self.coordinates[1][0]-1, self.coordinates[1][1]-1))
                rotatecoords.append((self.coordinates[3][0]-1, self.coordinates[3][1]+1))
                
                if rotatecoords[0] not in ground and rotatecoords[1] not in ground and rotatecoords[2] not in ground:
                
                    draw(self.coordinates, red)
                    
                    self.coordinates[0] = (self.coordinates[0][0]-2, self.coordinates[0][1]-2)
                    self.coordinates[1] = (self.coordinates[1][0]-1, self.coordinates[1][1]-1)
                    self.coordinates[3] = (self.coordinates[3][0]-1, self.coordinates[3][1]+1)
                       
                    draw(self.coordinates, self.color)
                    
                    return 0              
                        
    def move(self, direction):

        newarray = []

        def drawdirection(color):
            draw(self.coordinates, red)                            
            self.coordinates = [(y,x) for y,x in newarray]
            draw(self.coordinates, color)
       
        if direction == pygame.K_LEFT:
            newarray = [(y, x-1) for y,x in self.coordinates]
            if newarray[0][1] > -1 and newarray[1][1] > -1 and newarray[2][1] > -1 and newarray[3][1] > -1 and newarray[0] not in ground and newarray[1] not in ground and newarray[2] not in ground and newarray[3] not in ground:
                drawdirection(self.color)

        elif direction == pygame.K_RIGHT:
            newarray = [(y, x+1) for y,x in self.coordinates]
            if newarray[0][1] < 10 and newarray[1][1] < 10 and newarray[2][1] < 10 and newarray[3][1] < 10 and newarray[0] not in ground and newarray[1] not in ground and newarray[2] not in ground and newarray[3] not in ground:
                drawdirection(self.color)
        
    def movedown(self):
        newarray = []
        newarray = [(y+1, x) for y,x in self.coordinates]
        if newarray[0] not in ground and newarray[1] not in ground and newarray[2] not in ground and newarray[3] not in ground and newarray[0][0] < len(grid) and newarray[1][0] < len(grid) and newarray[2][0] < len(grid) and newarray[3][0] < len(grid):
            draw(self.coordinates, red)
            counter = 0
            self.coordinates = [(y,x) for y,x in newarray]
            draw(self.coordinates, self.color)
            
        else:
            return "change"
        
    def getdown(self):
        newarray = []
        newarray = [(y+1, x) for y,x in self.coordinates]
            
        if newarray[0] not in ground and newarray[1] not in ground and newarray[2] not in ground and newarray[3] not in ground and newarray[0][0] < len(grid) and newarray[1][0] < len(grid) and newarray[2][0] < len(grid) and newarray[3][0] < len(grid):
            draw(self.coordinates, red)        
            counter = 0                
            self.coordinates = [(y,x) for y,x in newarray]                
            draw(self.coordinates, self.color)            
            time.sleep(0.05)
            
        else:
            return "change"
        
    def returnlist(self):
        return self.coordinates
  
movedown = pygame.USEREVENT + 1
pygame.time.set_timer(movedown, 1000)
############################################################################################################################
def ScoreUpdate(multiplier):
    global font
    global score
    ScoreAddition = multiplier * 20
    score += ScoreAddition
    pygame.draw.rect(tetdisplay, black, (335, 322, 125, 75))
    pygame.display.update()
    img = font.render(str(score), True, blue)
    tetdisplay.blit(img, (360, 338))
    pygame.display.update()

def summonshape(sign2):
    
    if sign2 == "choose":
        
        blockinfo = random.choice(shapenames)
        
        if blockinfo == "cubeshape":
            return [[(0,3), (0,4), (1,3), (1,4)], green]
        
        if blockinfo == "sshape":
            return [[(0,3), (0,4), (1,2), (1,3)], blue]
        
        if blockinfo == "tshape":
            return [[(0,3), (0,4), (0,5), (1,4)], orange]
        
        if blockinfo == "straightlineshape":
            return [[(0,4), (1,4), (2,4), (3,4)], purple]
        
        if blockinfo == "lshape":
            return [[(0,4), (1,4), (2,4), (2,5)], white]
        
    else:
        if sign2 == "cubeshape":
            return [[(0,3), (0,4), (1,3), (1,4)], green]
    
        if sign2 == "sshape":
            return [[(0,3), (0,4), (1,2), (1,3)], blue]
        
        if sign2 == "tshape":
            return [[(0,3), (0,4), (0,5), (1,4)], orange]
        
        if sign2 == "straightlineshape":
            return [[(0,4), (1,4), (2,4), (3,4)], purple]
        
        if sign2 == "lshape":
            return [[(0,4), (1,4), (2,4), (2,5)], white]
            

def SortingFunctions(board):
    
    redcounter = 0
    cleanpile = []
    dirtpile = []
    
    def reground(board):
        global ground
        ground = []
        for row4 in board:
            lineindex = board.index(row4)
            for block4 in row4:
               blockindex3 = row4.index(block4)
               color = block4[1]
               if color != red:
                   ground.append((lineindex, blockindex3))
    
    def replace(board):
        newlist = []
        yr = 0
        xr = 608
        gridrange = 19
        for row3 in reversed(dirtpile):
            for block3 in row3:
                color = block3[1]
                newlist.append((pygame.draw.rect(tetdisplay, color, (yr, xr, 32, 32)), color))
                yr += 32
            board[gridrange] = newlist
            newlist = []
            gridrange -= 1
            pygame.display.update()
            yr = 0
            xr -=32
            
        for row2 in reversed(cleanpile):
            for block2 in row2:
                color = block2[1]
                newlist.append((pygame.draw.rect(tetdisplay, color, (yr, xr, 32, 32)), color))
                yr += 32
            board[gridrange] = newlist
            newlist = []
            gridrange -= 1
            pygame.display.update()
            yr = 0
            xr -=32
            reground(board)
        
    def reshuffle(board): #influenced by original grid code
        redcounter3 = 0
        for row in board:
            for block in row:
                color = block[1]
                if color == (255, 0, 0):
                    redcounter3 += 1
            if redcounter3 == 10:
                cleanpile.append(row)
                redcounter3 = 0
            elif redcounter3 < 10:
                dirtpile.append(row)
                redcounter3 = 0
        replace(board)

    def sort(board):
        redcounter2 = 0
        rowcounter = 0
        linescore = 0
        for row in reversed(board):
            for block in row:
                gridindex = board.index(row)
                color = block[1]
                if color == (255, 0, 0):
                    redcounter2 += 1
            if redcounter2 == 0:
                for block in row:
                    yc = block[0][0] # ((y, x, 32, 32), (255, 0, 0)) = y = yc
                    xc = block[0][1] # ((y, x, 32, 32), (255, 0, 0)) = x = xc
                    block = ((pygame.draw.rect(tetdisplay, red, (yc, xc, 32, 32)), red))
                    row[rowcounter] = block
                    rowcounter +=1
                board[gridindex] = row
                rowcounter = 0
                linescore += 1
                pygame.display.update()
            else:
                redcounter2 = 0
                continue
        score = ScoreUpdate(linescore)
        reshuffle(board)
            
    for row in reversed(board): #detects if there is a line that has no red in it
        for block in row:
            color = block[1]
            if color == (255, 0, 0):
                redcounter += 1
        if redcounter == 0: #if the program saw a line in the board that had no red, go to the next function
            sort(board)
            break
        else:
            redcounter = 0
            continue
    
def birthshape(coords):
    blockname = random.choice(shapenames)
    NextShape(BlockModelLibrary[blockname])
    currentshape = TetrisBlock(coords)
    result = False
    rotatecounter = 0
    sign = 0
    
    while currentshape: # main game loop
        
        global perspectiveshape
        
        keyspressed = pygame.key.get_pressed()
        if keyspressed[K_DOWN]:
            result = currentshape.getdown()
            
        for event in pygame.event.get():
            
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    currentshape.move(event.key)
                    
                if event.key == pygame.K_UP:                
                    sign = currentshape.rotate(sign)
                               
            if event.type == movedown:
                result = currentshape.movedown()
                
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                    
            elif result == "change": #this code gets signal to change the shape, and then changes it
                for tupe in currentshape.returnlist():
                    ground.append(tupe)
                SortingFunctions(grid)
                blockname1 = random.choice(shapenames)
                NextShape(BlockModelLibrary[blockname1])
                birthshape(summonshape(blockname))
                    
birthshape(summonshape("choose"))
pygame.display.update()