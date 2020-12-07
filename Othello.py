import time, random, ctypes, numpy, math
from pygame import gfxdraw
import pygame as p
ctypes.windll.user32.SetProcessDPIAware()

width = 8
height = 8

size = 110

movelist = []
colors = [(0,144,103),(255,255,255),(70,70,70),(255,0,0),(0,0,0)]
radi = int(size/2)
halfwi = int(width/2)
halfhe = int(height/2)

arr = [[0 for i in range(width)] for j in range(height)]

p.init()
window = p.display.set_mode((size*width,size*height))
p.display.set_caption('Othello!') 
watch = p.time.Clock()

def circle(x,y,r,col):
    x = int(size*x)+radi
    y = int(size*y)+radi
    gfxdraw.aacircle(window,x,y,r,colors[col])
    gfxdraw.filled_circle(window,x,y,r,colors[col])

def human():
    x,y = p.mouse.get_pos()
       
    y = math.floor(y/size)
    x = math.floor(x/size)

    if(arr[y][x] == -2):
        arr[y][x] = -1
        if(update(y,x,1) == False):
            robot()

def robot():
    if(len(movelist) > 0):
        choice = random.choice(movelist)
        y,x = choice[0],choice[1]

        if(arr[y][x] == 2):
            time.sleep(0.5)
            arr[y][x] = 1
            update(y,x,-1)

def ab(y,x,nr):
    if(nr == 0 and y == 0 or nr == 2 and x == 0): return 0
    elif(nr == 0 or nr == 2): return -1

    if(nr == 1 and y == height-1 or nr == 3 and x == width-1): return 1
    elif(nr == 1 or nr == 3): return 2

def remove(reset):
    for j in range(0,height):
        for i in range(0,width):

            val = arr[j][i]

            if(reset): arr[j][i] = 0

            if(val == 2 or val == -2 or reset): arr[j][i] = 0

def flip(j,i,n):

    cache = []

    for b in range(ab(j,i,0),ab(j,i,1)):
        for a in range(ab(j,i,2),ab(j,i,3)):

            if(arr[j+b][i+a] == n):

                index = 1
                jval = j+index*b
                ival = i+index*a

                while(0 <= jval < height and 0 <= ival < width and arr[jval][ival] == n):
                    cache.append(jval)
                    cache.append(ival)
                    index += 1
                    jval = j+index*b
                    ival = i+index*a

                if(0 <= jval < height and 0 <= ival < width and arr[jval][ival] == -1*n):
                    for k in range(0,int(len(cache)/2)):
                        arr[cache[k*2]][cache[k*2+1]] = -1*n
                cache = []

def moves(n):
    global movelist
    movelist = []
    for j in range(0,height):
        for i in range(0,width):
        
            if(arr[j][i] == n):

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

def check(n):
    white = 0
    black = 0
    moves = 0
    empty = 0
    space = int(width*size/18)

    for j in range(0,height):
        for i in range(0,width):
            
            val = arr[j][i]

            if(val == -1): black += 1

            elif(val == 1):  white += 1

            else: empty += 1

            if(val == 2*n): moves += 1

    p.display.set_caption('Othello!'+(' '*space)+'Black: '+str(black)+'        White: '+str(white))
    
    if(empty == 0 or moves == 0 or black == 0 or white == 0): return True 

def write(y,x,red):

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
    if(red):
        circle(x,y,int(radi/8),3)

    p.display.flip()

def update(y,x,n):
    
    remove(False)

    flip(y,x,n)
    
    moves(n)

    write(y,x,True)

    if(check(n)):
        time.sleep(3)
        remove(True)
        start()
        return True 
    else: return False

def start():
    for i in range(0,2):
        arr[halfhe-i][halfwi-i] = 1
        arr[halfhe+(0-i)][halfwi+(i-1)] = -1

    moves(-1)
    write(0,0,False)

start()
run = True
while(run):

    for event in p.event.get():

        if(event.type == p.QUIT):
            run = False

        elif(event.type == p.MOUSEBUTTONDOWN):
            human()

    watch.tick(10)