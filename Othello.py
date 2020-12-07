import time, random, ctypes, numpy, math
from pygame import gfxdraw
import pygame as p
ctypes.windll.user32.SetProcessDPIAware()

width = 8
height = 8

size = 110

movelist = []
colors = [(0,144,103),(255,255,255),(70,70,70),(255,0,0),(0,0,0)]
halfhe = int(height/2)
halfwi = int(width/2)
radi = int(size/2)
player = True
reset = False
tick = 0

arr = [[0 for i in range(width)] for j in range(height)]

for i in range(0,2):
    arr[halfhe-i][halfwi-i] = 1
    arr[halfhe+(0-i)][halfwi+(i-1)] = -1

p.init()
window = p.display.set_mode((size*width,size*height))
p.display.set_caption('Othello!') 
watch = p.time.Clock()

def ab(y,x,nr):
    if(nr == 0 and y == 0 or nr == 2 and x == 0): return 0
    elif(nr == 0 or nr == 2): return -1

    if(nr == 1 and y == height-1 or nr == 3 and x == width-1): return 1
    elif(nr == 1 or nr == 3): return 2

def circle(x,y,r,col):
    x = int(size*x)+radi
    y = int(size*y)+radi
    gfxdraw.aacircle(window,x,y,r,colors[col])
    gfxdraw.filled_circle(window,x,y,r,colors[col])

def human():
    if(len(movelist) > 0):
        x,y = p.mouse.get_pos()

        y = math.floor(y/size)
        x = math.floor(x/size)

        if(arr[y][x] == -2):
            arr[y][x] = -1
            if(update(y,x,1)): return True
    else:
        update(height,width,1)
    
def robot():
    if(len(movelist) > 0):
        choice = random.choice(movelist)

        y = choice[0]
        x = choice[1]

        if(arr[y][x] == 2):
            time.sleep(0.5)
            arr[y][x] = 1
            if(update(y,x,-1)): return True
    else:
        update(height,width,-1)

def remove(reset):
    for j in range(0,height):
        for i in range(0,width):

            if(arr[j][i] == -2 or arr[j][i] == 2 or reset): arr[j][i] = 0
    
    if(reset):
        for i in range(0,2):
            arr[halfhe-i][halfwi-i] = 1
            arr[halfhe+(0-i)][halfwi+(i-1)] = -1

def flip(j,i,n):
    cache = []

    for b in range(ab(j,i,0),ab(j,i,1)):
        for a in range(ab(j,i,2),ab(j,i,3)):

            if(arr[j+b][i+a] == n):

                index = 1
                jval,ival = j+index*b,i+index*a

                while(0 <= jval < height and 0 <= ival < width and arr[jval][ival] == n):
                    cache.append([jval,ival])
                    index += 1
                    jval,ival = j+index*b,i+index*a

                if(0 <= jval < height and 0 <= ival < width and arr[jval][ival] == -1*n):
                    for k in range(len(cache)):
                        arr[cache[k][0]][cache[k][1]] = -1*n
                cache = []

def moves(n):
    global movelist
    white = 0
    black = 0
    empty = 0
    space = int(width*size/18)
    movelist = []

    for j in range(0,height):
        for i in range(0,width):
            
            val = arr[j][i]

            if(val == n):

                for b in range(ab(j,i,0),ab(j,i,1)):
                    for a in range(ab(j,i,2),ab(j,i,3)):

                        if(arr[j+b][i+a] == -1*n):
                            
                            index = 1
                            jval,ival = j+index*b,i+index*a

                            while(0 <= jval < height and 0 <= ival < width and arr[jval][ival] == -1*n):
                                index += 1
                                jval,ival = j+index*b,i+index*a

                            if(0 <= jval < height and 0 <= ival< width and arr[jval][ival] == 0):
                                arr[jval][ival] = 2*n
                                movelist.append([jval,ival])

            if(val == -1): black += 1

            elif(val == 1):  white += 1

            else: empty += 1
    
    p.display.set_caption('Othello!'+(' '*space)+'Black: '+str(black)+'        White: '+str(white))
    
    if(white == 0 or black == 0 or empty == 0): return True 

def write(y,x):
    window.fill(colors[0])

    for i in range(0,2):
        circle(((halfwi-2.5)+i*4),((halfhe-2.5)+i*4),int(radi/8),4)
        circle((halfwi+(1.5-i*4)),(halfhe+(i*4-2.5)),int(radi/8),4)

    for j in range(0,height):

        if(j <= height-2): 
            gfxdraw.hline(window,0,height*size,(j+1)*size,colors[4])

        for i in range(0,width):
            if(j == 0 and i <= width-2): 
                gfxdraw.vline(window,(i+1)*size,0,width*size,colors[4])
            
            n = arr[j][i]
            if(n != 0):

                if(n == -1 or n == 1):
                    circle(i,j,radi-5,2)
                    circle(i,j,radi-7,n)

                elif(n == -2):
                    circle(i,j,radi-5,2)
                    circle(i,j,radi-7,0)

    if(x < width and y < height):
        circle(x,y,int(radi/8),3)

    p.display.flip()

def update(y,x,n):
    remove(False)

    if(x < width and y < height):
        flip(y,x,n)
    
    if(moves(n)):
        write(height,width)
        return True
    else:
        write(y,x)

def start():
    moves(-1)
    write(height,width)

def restart():
    remove(True)
    start()

run = True
start()
while(run):
    
    if(player == False):
        if(robot()): reset = True
        player = True

    for event in p.event.get():

        if(event.type == p.QUIT):
            run = False

        if(event.type == p.MOUSEBUTTONDOWN):
            if(reset):
                player = True
                reset = False
                restart()

            elif(player):
                if(human()): reset = True
                else: player = False

    watch.tick(10)