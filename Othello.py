import time, random, ctypes, numpy, math
import pygame as p
ctypes.windll.user32.SetProcessDPIAware()

width = 8
height = 8

size = 100

colors = [(0,0,0),(255,255,255),(0,144,103),(70,70,70)]
ry = random.randint(0,height-1)
rx = random.randint(0,width-1)
radi = int(size/2)
tick = 0
player = True

arr = [[0 for i in range(width)] for j in range(height)]

for i in range(0,2):
    arr[int(height/2-i)][int(width/2-i)] = 1
    arr[int(height/2+(0-i))][int(width/2+(i-1))] = -1

p.init()
window = p.display.set_mode((size*width,size*height))
p.display.set_caption('Othello!') 
watch = p.time.Clock()

run = True
while(run):
    tick += 1

    if(player == False):

        while(arr[ry][rx] < 2):
            ry = random.randint(0,height-1)
            rx = random.randint(0,width-1)

        time.sleep(0.5)
        arr[ry][rx] = 1

        for b in range(-1,2):
            for a in range(-1,2):

                if(ry+b >= 0 and ry+b < height and rx+a >= 0 and rx+a < width and arr[rx+a][ry+b] == -1):
                                
                    index = 1
                    while(ry+b*index >= 0 and ry+b*index < height and rx+a*index >= 0 and rx+a*index < width and arr[ry+b*index][rx+a*index] == -1):
                        cache.append(ry+b*index)
                        cache.append(rx+a*index)
                        index += 1

                    if(arr[ry+b*index][rx+a*index] == 1):
                        for i in range(0,int(len(cache)/2)):
                            arr[cache[i*2]][cache[i*2+1]] = 1
                    cache = [] 
        player = True           
        
    for event in p.event.get():

        if(event.type == p.QUIT):
            run = False

        elif(event.type == p.MOUSEBUTTONDOWN and player):
            x,y = p.mouse.get_pos()
            
            y = math.floor(y/size)
            x = math.floor(x/size)
            
            if(arr[y][x] == -2):
                arr[y][x] = -1
                cache = []

                for b in range(-1,2):
                    for a in range(-1,2):

                        if(y+b >= 0 and y+b < height and x+a >= 0 and x+a < width and arr[x+a][y+b] == 1):
                                
                            index = 1
                            while(y+b*index >= 0 and y+b*index < height and x+a*index >= 0 and x+a*index < width and arr[y+b*index][x+a*index] == 1):
                                cache.append(y+b*index)
                                cache.append(x+a*index)
                                index += 1

                            if(arr[y+b*index][x+a*index] == -1):
                                for i in range(0,int(len(cache)/2)):
                                    arr[cache[i*2]][cache[i*2+1]] = -1
                                    print("JA")
                                cache = []            
                player = False

    window.fill(colors[2])
    for j in range(0,height):

        if(j <= width-1): p.draw.line(window,colors[0],(0,(j+1)*size),((width+1)*size,(j+1)*size),2)

        for i in range(0,width):
            if(j == 0 and i <= width-1): p.draw.line(window,colors[0],((i+1)*size,0),((i+1)*size,(height+1)*size),2)
            
            value = arr[j][i]
            if(value != 0):

                if(-2 < value < 2):
                    p.draw.circle(window,colors[int((1+value)/2)],(i*size+radi+1,j*size+radi+1),radi-5)

                    for b in range(-1,2):
                        for a in range(-1,2):
                            try:
                                if(j+b >= 0 and j+b < height and i+a >= 0 and i+a < width and arr[j+b][i+a] == -1*value):
                                    
                                    index = 1
                                    while(j+b*index >= 0 and j+b*index < height and i+a*index >= 0 and i+a*index < width and arr[j+b*index][i+a*index] == -1*value):
                                        index += 1

                                    if(arr[j+b*index][i+a*index] == 0):
                                        arr[j+b*index][i+a*index] = value*2
                            except:
                                pass

                elif(value == -2): 
                    p.draw.circle(window,colors[3],(i*size+radi+1,j*size+radi+1),radi-2,2)

    watch.tick(60)
    p.display.flip()