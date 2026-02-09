import pygame
import random
import time
import math
from line_profiler import LineProfiler
profiler = LineProfiler()

 
pygame.init()
 
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue=(70,50,255)
purple=(120,50,255)
green=(100,255,150)


dis_width = 780
dis = pygame.display.set_mode((dis_width, dis_width))
pygame.display.set_caption('Змейка от Skillbox')


font_style = pygame.font.SysFont(None, 30)
def masag(msg,color,x1,y1): 
   mesg = font_style.render(msg, True, color)
   dis.blit(mesg, [x1, y1])

def ris_zm(snake_block,dlin_zm,x1,y1):
    for i in range(len(dlin_zm)-1,0,-1):
        if i!=0:
            dlin_zm[i]=dlin_zm[i-1]
            x11,y11=dlin_zm[i]
            pygame.draw.circle(dis, black, (x11, y11), snake_block-3)  
    
    dlin_zm[0]=[x1,y1]
    x11,y11=dlin_zm[0]
    pygame.draw.circle(dis, black, (x11, y11), snake_block-3)

def pola(x1,y1):
    if x1 >= dis_width or x1 <= 0 or y1 >= dis_width or y1 <= 0:
            return True 

def bespola(x1,y1):
    if x1 >= dis_width:
        x1=0
    elif x1 <= 0-0.1:
        x1=dis_width
    elif y1 >= dis_width:
        y1=0
    elif y1 <= 0-0.1:
        y1=dis_width
    return x1, y1

x_ra=[]
y_ra=[]
high=[]
width=[]
def pripat(dis_width):
    for i in range(10):
        x_ra.append(random.randrange(10, dis_width-10, 10))
        y_ra.append(random.randrange(10, dis_width-10, 10))
        high.append(random.randrange(10, 60, 10))
        width.append(random.randrange(50, 60, 10))

#Общая разметка поля
obch_rasm=[]
for x in range(0,780,10):
    for y in range(0,780,10):
        obch_rasm.append(pygame.draw.rect(dis,red,(x,y,10,10)))

def uvelich(dlin_zm,pribav,x,y):
    if pribav==1 and (x!=dlin_zm[len(dlin_zm)-1][0] or y!=dlin_zm[len(dlin_zm)-1][1]):
        pygame.draw.circle(dis,black,(x,y),10)
    elif pribav!=2:
        pribav=0
    if pribav==0:
        pygame.draw.circle(dis,black,(x,y),10)
    if pribav==0:
        dlin_zm.append([])
        pribav=2
    return pribav

def na_prepat(b,dis_width):
    n=0
    x=random.randrange(20, dis_width-20, 10)
    y=random.randrange(20, dis_width-20, 10)
    while n==0:
        for i in b:    
            if i.collidepoint(x,y):
                x=random.randrange(20, dis_width-20, 10)
                y=random.randrange(20, dis_width-20, 10)
                n=2
                break
        if n!=2:
            n=1
        else:
            n=0
    return x,y

def sov_so_zm(dlin_zm,x,y):
    n=0
    while n==0:
        for i in dlin_zm: 
            x2=i[0]
            y2=i[1]   
            if abs(x2-x)>20 or abs(y2-y)>20:
                x=random.randrange(20, dis_width-20, 10)
                y=random.randrange(20, dis_width-20, 10)
                n=2
                break
        if n!=2:
            n=1
        else:
            n=0
    return x,y

def dvish_ed(x1,y1,x_rand,y_rand):
    nacon=[[x_rand,y_rand],[x1,y1]]
    cor_toch=[]
    promesh=[]
    for i in obch_rasm:
        if i.clipline(nacon[0],nacon[1]):
            for j,c in enumerate(i):
                if j in (0,1):
                    promesh.append(c)
            cor_toch.append(promesh)
            promesh=[]
    return cor_toch

#Все функции раньше
vopr=4
dis.fill(blue)
x,y=[0,0]
while vopr==4:
    a1=pygame.draw.rect(dis,purple,[300,156,400,100])
    masag('без полей и без припятствий',red,300,156)
    a2=pygame.draw.rect(dis,purple,[300,312,400,100])
    masag('без полей и с припятствий',red,300,312)
    a3=pygame.draw.rect(dis,purple,[300,468,400,100])
    masag('с полями и без припятствий',red,300,468)
    a4=pygame.draw.rect(dis,purple,[300,624,400,100])
    masag('с полями и с припятствий',red,300,624)
    pygame.display.update()
    for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y=pygame.mouse.get_pos()
    nashat=[a1,a2,a3,a4]
    for i,nom in enumerate(nashat):
        if nom.collidepoint(x,y):
            vopr=i
    
def bespripat():
    time_0=time.time()
    cor_toch=[]
    nachal_dvish=0
    x=0
    pribav=0
    kor_prip=[]
    x_rand=0.5
    x1=0.5
    game_over = False
    snake_block=10 
    magn=pygame.draw.circle(dis, green, (200, 200), snake_block+5)
    x1_change = 0
    y1_change = 0
    clock = pygame.time.Clock()
    rand_vr=random.randrange(10, 40, 10)
    snake_speed=10
    dlin_zm=[[]]
    game_close=False
    dis.fill(blue)
    #рисует припятствия
    if vopr ==1 or vopr == 3:
        pripat(dis_width)
        for i in range(10):
            kor_prip.append(pygame.draw.rect(dis, purple, [x_ra[i], y_ra[i], high[i], width[i]]))
    pygame.display.update()
    x_rand_magn,y_rand_magn=na_prepat(kor_prip,dis_width)
    #Первая точка еды
    while x_rand==0.5:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x_rand,y_rand=pygame.mouse.get_pos()
    x_rand=round(x_rand)+(10-int(str(round(x_rand))[-1:]))
    y_rand=round(y_rand)+(10-int(str(round(y_rand))[-1:]))
    pygame.draw.circle(dis, red, (x_rand, y_rand), snake_block)
    pygame.display.update()
    #Первый круг змейки
    while x1==0.5:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x1,y1=pygame.mouse.get_pos()
    x1=round(x1)+(10-int(str(round(x1))[-1:]))
    y1=round(y1)+(10-int(str(round(y1))[-1:]))
    pygame.draw.circle(dis, black, (x1, y1), snake_block)  
    pygame.display.update()

    while not game_over:
        while game_close==True:
            masag('Вы проиграли: нажмите P чтобы продолжить или C чтобы сброить',red,dis_width/10,dis_width/3)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_p:
                        bespripat()
        n=1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if n==0:
                break
            n=0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change != snake_block:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change != -snake_block:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change != snake_block:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change != -snake_block:
                    y1_change = snake_block
                    x1_change = 0
        x1 += x1_change
        y1 += y1_change 
        dis.fill(blue)
        
        #Временной промежуток магнита
        time_1=time.time()
        if rand_vr <= time_1-time_0 <= rand_vr+15-math.sqrt(snake_speed) and not(magn.collidepoint(x1,y1)):
            magn=pygame.draw.circle(dis, green, (x_rand_magn, y_rand_magn), snake_block+5)
        elif magn.collidepoint(x1,y1):
            time_0=time.time()
            x_rand_magn,y_rand_magn=na_prepat(kor_prip,dis_width)
            x_rand_magn, y_rand_magn=sov_so_zm(dlin_zm,x_rand_magn, y_rand_magn)
            nachal_dvish=1
            rand_vr=random.randrange(10, 40, 10)
        if nachal_dvish==1:
            chet=0
            cor_toch=dvish_ed(x1,y1,x_rand,y_rand)
            if x_rand>x1:
                cor_toch=sorted(cor_toch,reverse=True)
            elif x_rand==x1 and y_rand>y1:
                cor_toch=sorted(cor_toch,reverse=True)
            if chet<len(cor_toch)-1:
                chet+=1
            if len(cor_toch)!=0:
                x_rand,y_rand=cor_toch[chet]
            else:
                nachal_dvish=0
            if x1 == x_rand and y1 == y_rand:
                nachal_dvish=0
        else:
            nachal_dvish=0

        #Рисует припятствия
        if vopr ==1 or vopr == 3:
            for i in range(10):
                pygame.draw.rect(dis, purple, [x_ra[i], y_ra[i], high[i], width[i]])
            for i in kor_prip:    
                if i.collidepoint(x1,y1):
                    game_close=True
        #Проверка на поля
        if vopr==2:
            game_close=pola(x1,y1)
        #Это нужно,чтобы были препятствия
        elif vopr==3 and game_close!=True:
            game_close=pola(x1,y1)
        else:
            x1,y1=bespola(x1,y1) 

        #Рисует еду, съел еду
        pygame.draw.circle(dis, red, (x_rand, y_rand), snake_block)
        if x1 == x_rand and y1 == y_rand:    
            x_rand, y_rand=na_prepat(kor_prip,dis_width)
            x_rand, y_rand=sov_so_zm(dlin_zm,x_rand, y_rand)
            pribav=1
            nachal_dvish=0
            x,y=[x1,y1]
            if ((len(dlin_zm)-1)%10==5 or (len(dlin_zm)-1)%10==0) and len(dlin_zm)>2 and snake_speed!=60:
                snake_speed+=5

        #Движение змейки, проверкаа на хвост
        ris_zm(snake_block,dlin_zm,x1,y1)
        if x!=0:
            pribav=uvelich(dlin_zm,pribav,x,y)
        n=0
        if len(dlin_zm)>1:
            for i in dlin_zm:
                n+=1
                if n != 1:
                    if i==[x1,y1]:
                        game_close = True
        
        pygame.display.update()
        clock.tick(snake_speed)

    dis.fill(blue)
    masag(f'ваш счёт {len(dlin_zm)}',red,dis_width/3,dis_width/3)
    pygame.display.update()
    clock.tick(2)
    pygame.quit()
bespripat()
profiler.print_stats()
quit()




