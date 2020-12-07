import time, random, ctypes, numpy, math
import pygame as p
ctypes.windll.user32.SetProcessDPIAware()

width = 8
height = 8

size = 100
tick = 0

colors = [(0,0,0),(255,255,255),(0,144,103),(70,70,70)]
ry = random.randint(0,height-1)
rx = random.randint(0,width-1)
radi = int(size/2)
player = True

arr = [[0 for i in range(width)] for j in range(height)]

for i in range(0,2):
    arr[int(height/2-i)][int(width/2-i)] = 1
    arr[int(height/2+(0-i))][int(width/2+(i-1))] = -1

p.init()
window = p.display.set_mode((size*width,size*height))
p.display.set_caption('Othello!') 
watch = p.time.Clock()

def robot():
    global ry,rx,player
    while(arr[ry][rx] < 2):
        ry = random.randint(0,height-1)
        rx = random.randint(0,width-1)

    arr[ry][rx] = 1
    player = True   
    flip(ry,rx,1)

def human():
    global y,x,player
    x,y = p.mouse.get_pos()
            
    y = math.floor(y/size)
    x = math.floor(x/size)
            
    if(arr[y][x] == -2):
        arr[y][x] = -1
        player = False
        flip(y,x,-1)

def flip(y,x,value):
    for b in range(-1,2):
        for a in range(-1,2):
            try:
                if(arr[x+a][y+b] == -1*value):

                    index = 1
                    while(arr[y+b*index][x+a*index] == -1*value):
                        cache.append(y+b*index)
                        cache.append(x+a*index)
                        index += 1

                    if(arr[y+b*index][x+a*index] == value):
                        for i in range(0,int(len(cache)/2)):
                            arr[cache[i*2]][cache[i*2+1]] = value
                    cache = []
            except:
                pass

def check(y,x,value):
    for b in range(-1,2):
        for a in range(-1,2):
            try:
                print("Ja")
                if(arr[y+b][x+a] == -1*value):

                    index = 1
                    while(arr[y+b*index][x+a*index] == -1*value):
                        index += 1

                    if(arr[y+b*index][x+a*index] == 0):
                        arr[y+b*index][x+a*index] = value*2
            except:
                pass

def write():
    window.fill(colors[2])
    for j in range(0,height):

        if(j <= width-1): 
            p.draw.line(window,colors[0],(0,(j+1)*size),((width+1)*size,(j+1)*size),2)

        for i in range(0,width):
            if(j == 0 and i <= width-1): 
                p.draw.line(window,colors[0],((i+1)*size,0),((i+1)*size,(height+1)*size),2)
            
            value = arr[j][i]
            if(value != 0):

                if(-2 < value < 2):
                    p.draw.circle(window,colors[int((1+value)/2)],(i*size+radi+1,j*size+radi+1),radi-5)
                    check(j,i,value)
                
                else:
                    if(value == -2):
                        p.draw.circle(window,colors[3],(i*size+radi+1,j*size+radi+1),radi-2,2)
                    arr[j][i] = 0

run = True
while(run):
    tick += 1

    if(player == False):
        robot()
        
    for event in p.event.get():

        if(event.type == p.QUIT):
            run = False

        elif(event.type == p.MOUSEBUTTONDOWN and player):
            human()

    write()

    if(tick%180 == 0):
        print(numpy.array(arr))


    watch.tick(60)
    p.display.flip()