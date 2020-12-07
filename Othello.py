import time, random, ctypes, numpy, math
import pygame as p
ctypes.windll.user32.SetProcessDPIAware()

width = 8
height = 8

size = 100
turn = -1

colors = [(0,144,103),(255,255,255),(70,70,70),(0,0,0)]
radi = int(size/2)
player = True

arr = [[0 for i in range(width)] for j in range(height)]

for i in range(0,2):
    arr[int(height/2-i)][int(width/2-i)] = 1
    arr[int(height/2+(0-i))][int(width/2+(i-1))] = -1

arr[2][3] = 2
arr[3][2] = 2 
arr[4][5] = 2
arr[5][4] = 2


p.init()
window = p.display.set_mode((size*width,size*height))
p.display.set_caption('Othello!') 
watch = p.time.Clock()

def robot():
    global y,x,player
    while(arr[y][x] < 2):
        y = random.randint(0,height-1)
        x = random.randint(0,width-1)

    arr[y][x] = 1  
    turn = 1
    update()
    player = True

def human():
    global y,x,player
    x,y = p.mouse.get_pos()
            
    y = math.floor(y/size)
    x = math.floor(x/size)
            
    if(arr[y][x] == 2):
        arr[y][x] = -1
        turn = -1
        update()
        player = False

def corner(j,i):
    global nj,pj,ni,pi
    nj,pj = -1,2
    ni,pi = -1,2

    tj = round(j/(height-1),1)
    ti = round(i/(width-1),1)

    if(tj == 0.0): nj = 0
    if(tj == 1.0): pj = 1
    if(ti == 0.0): ni = 0
    if(ti == 1.0): pi = 1

def flip():
    global turn,nj,pj,ni,pi

    corner(y,x)

    for b in range(nj,pj):
        for a in range(ni,pi):
            try:
                if(arr[y+b][x+a] == -1*turn):

                    index = 1
                    while(arr[y+b*index][x+a*index] == -1*turn):
                        cache.append(y+b*index)
                        cache.append(x+a*index)
                        index += 1

                    if(arr[y+b*index][x+a*index] == turn):
                        for i in range(0,int(len(cache)/2)):
                            arr[cache[i*2]][cache[i*2+1]] = turn
                        cache = []
            except:
                pass

def update():
    global player,turn,nj,pj,ni,pi

    for j in range(0,height):
        for i in range(0,width):
            if(arr[j][i] == 2):
                arr[j][i] = 0

    flip()
    
    for j in range(0,height):
        for i in range(0,width):

            if(arr[j][i] == turn):

                corner(j,i)

                for b in range(nj,pj):
                    for a in range(ni,pi):

                        if(arr[j+b][i+a] == -1*turn):
                            
                            index = 1
                            while(j+index*b < height and i+index*a < width and arr[j+b*index][i+a*index] == -1*turn):
                                index += 1
                                
                            if(j+index*b < height and i+index*a < width and arr[j+b*index][i+a*index] == 0):
                                arr[j+b*index][i+a*index] = 2

def write():
    window.fill(colors[0])
    for j in range(0,height):

        if(j <= width-1): 
            p.draw.line(window,colors[3],(0,(j+1)*size),((width+1)*size,(j+1)*size),2)

        for i in range(0,width):
            if(j == 0 and i <= width-1): 
                p.draw.line(window,colors[3],((i+1)*size,0),((i+1)*size,(height+1)*size),2)
            
            value = arr[j][i]
            if(value != 0):

                if(value == -1 or value == 1):
                    p.draw.circle(window,colors[value],(i*size+radi+1,j*size+radi+1),radi-5)

                elif(value == 2 and player):
                    p.draw.circle(window,colors[2],(i*size+radi+1,j*size+radi+1),radi-2,2)

run = True
while(run):

    write()

    if(player == False):
        robot()
        
    for event in p.event.get():

        if(event.type == p.QUIT):
            run = False

        elif(event.type == p.MOUSEBUTTONDOWN and player):
            human()

    watch.tick(60)
    p.display.flip()