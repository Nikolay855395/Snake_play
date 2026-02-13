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
yellow = (255, 255, 0) 
tusk_yellow=(100,100,0)
dark_blue=(0,0,255)
pink=(255,192,203)

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

def pripat(dis_width,x_ra,y_ra,high,width):
    for i in range(10):
        x_ra.append(random.randrange(10, dis_width-10, 10))
        y_ra.append(random.randrange(10, dis_width-10, 10))
        high.append(random.randrange(10, 60, 10))
        width.append(random.randrange(50, 60, 10))

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

def na_prepat(b,x_rand,y_rand):
    n=0
    for i in b:    
        if i.collidepoint(x_rand,y_rand):
            n=2
            break
    return n

def sov_so_zm(kor_sentr,b,x,y):
    x_centr,y_centr=kor_sentr
    kx=x_centr-x
    ky=y_centr-y
    try:
        mnx=kx//abs(kx)
    except ZeroDivisionError:
        mnx=0
    try:
        mny=ky//abs(ky)
    except ZeroDivisionError:
        mny=0
    if mnx<=0:
        mnx=0
    if mny<=0:
        mny=0
    n=2
    while n==2:
        x_rand=random.randrange((x_centr)*mnx+10, x_centr+(x_centr)*mnx-10,10)
        y_rand=random.randrange((y_centr)*mny+10, y_centr+(y_centr)*mny-10,10)
        n=na_prepat(b,x_rand,y_rand)
    return x_rand,y_rand

def dvish_ed(x1,y1,x_rand,y_rand,snake_block):
    dx=x1-x_rand
    dy=y1-y_rand
    G=(dx**2 + dy**2)**0.5
    x_rand+=((dx)/G)*2
    y_rand+=((dy)/G)*2
    circle=pygame.draw.circle(dis, red, (x_rand, y_rand), snake_block)
    return x_rand,y_rand,circle

#Все функции раньше
dis.fill(blue)
def vibor():
    vopr=4
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
    return vopr
def bespripat():
    x_ra=[]
    y_ra=[]
    high=[]
    width=[]
    vopr=vibor()
    time_0_m=time.time()
    time_0_p=time.time()
    kor_sentr=[dis_width//2,dis_width//2]
    propusk=0
    dostup_portal=0
    nachal_dvish=0
    portal_1=0
    x=0
    pribav=0
    kor_prip=[]
    x_rand=0.5
    x1=0.5
    game_over = False
    snake_block=10 
    x1_change = 0
    y1_change = 0
    clock = pygame.time.Clock()
    rand_vr_m=random.randrange(10, 20, 10)
    rand_vr_p=random.randrange(10, 40, 10)
    snake_speed=10
    dlin_zm=[[]]
    game_close=False
    dis.fill(blue)
    #рисует припятствия
    if vopr ==1 or vopr == 3:
        pripat(dis_width,x_ra,y_ra,high,width)
        for i in range(10):
            kor_prip.append(pygame.draw.rect(dis, purple, [x_ra[i], y_ra[i], high[i], width[i]]))
    pygame.display.update()
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
                        dis.fill(blue)
                        vopr=vibor()
                        bespripat()
        n=1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if n==0:
                break
            n=0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    if dostup_portal!=0:
                        dostup_portal-=1
                        x1,y1=[-1,-1]
                        dis.fill(black)
                        pygame.display.update()
                        tim_chet=0
                        while x1==-1 and y1==-1:
                            if tim_chet<=600:
                                for i in range(len(x_ra)):
                                    pygame.draw.rect(dis, yellow, [x_ra[i], y_ra[i], high[i], width[i]])
                                pygame.draw.circle(dis, blue, (x_rand, y_rand), snake_block)
                                pygame.draw.circle(dis, red, (390, 390), snake_block)
                                pygame.draw.circle(dis, red, (390+x1_change*2, 390+y1_change*2), snake_block-5)
                                tim_chet+=1
                            elif tim_chet<=1200:
                                for i in range(len(x_ra)):
                                    pygame.draw.rect(dis, tusk_yellow, [x_ra[i], y_ra[i], high[i], width[i]])
                                pygame.draw.circle(dis, dark_blue, (x_rand, y_rand), snake_block)
                                pygame.draw.circle(dis, pink, (390, 390), snake_block)
                                pygame.draw.circle(dis, pink, (390+x1_change*2, 390+y1_change*2), snake_block-5)
                                tim_chet+=1
                            else:
                                tim_chet=0
                            pygame.display.update()
                            for event in pygame.event.get():
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    x1,y1=pygame.mouse.get_pos()
                                    x1=round(x1)+(10-int(str(round(x1))[-1:]))
                                    y1=round(y1)+(10-int(str(round(y1))[-1:]))
                                    portal_1=1
                                    x_rand_port_v,y_rand_port_v=x1,y1
                                    propusk=1
                    else:
                        masag('У вас недостаточно энергии',red,300,312)
                        pygame.display.update()
                        time.sleep(4)
                elif event.key == pygame.K_LEFT and x1_change != snake_block:
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
        if propusk==0:
            x1 += x1_change
            y1 += y1_change 
        else:
            propusk=0
        dis.fill(blue)

        #Красивый выход
        if portal_1==1:
            if [x_rand_port_v,y_rand_port_v] != dlin_zm[len(dlin_zm)-1]:
                pygame.draw.circle(dis,black,(x_rand_port_v,y_rand_port_v),20)
                pygame.draw.circle(dis,red,(x_rand_port_v-10,y_rand_port_v),5)
                pygame.draw.circle(dis,red,(x_rand_port_v+10,y_rand_port_v),5)
            else:
                portal_1=0
        
        #Временной промежуток магнита
        time_1=time.time()
        if rand_vr_m-0.1 <= time_1-time_0_m <= rand_vr_m:
            x_rand_magn, y_rand_magn=sov_so_zm(kor_sentr,kor_prip,x1, y1)
        if rand_vr_m <= time_1-time_0_m <= rand_vr_m+15-math.sqrt(snake_speed) and nachal_dvish==0:
            magn=pygame.draw.circle(dis, green, (x_rand_magn, y_rand_magn), snake_block+5)
        try:
            if magn.collidepoint(x1,y1):
                magn=0
                nachal_dvish=1
            elif not(time_1-time_0_m <= rand_vr_m+15-math.sqrt(snake_speed)):
                time_0_m=time.time()
                magn=0
        except UnboundLocalError:
            nachal_dvish=0
        except AttributeError: 
            magn=0
        if nachal_dvish==1:
            x_rand,y_rand,circle=dvish_ed(x1,y1,x_rand,y_rand,snake_block)

        #Рандомное время портала
        if rand_vr_p-0.1 <= time_1-time_0_p <= rand_vr_p:
            x_rand_port,y_rand_port=sov_so_zm(kor_sentr,kor_prip,x1, y1)
        if rand_vr_p <= time_1-time_0_p <= rand_vr_p+15-math.sqrt(snake_speed):
            portal=pygame.draw.circle(dis,black,(x_rand_port,y_rand_port),20)
            pygame.draw.circle(dis,yellow,(x_rand_port-10,y_rand_port),5)
            pygame.draw.circle(dis,yellow,(x_rand_port+10,y_rand_port),5)
        try:
            if portal.collidepoint(x1,y1):
                portal=0
                time_0_p=time.time()
                rand_vr_p=random.randrange(10, 40, 10)
                dostup_portal+=1
            elif time_1-time_0_p > rand_vr_p+15-math.sqrt(snake_speed):
                time_0_p=time.time()
                rand_vr_p=random.randrange(10, 40, 10)
                portal=0
        except UnboundLocalError:
            portal=0
        except AttributeError: 
            portal=0

        #Рисует припятствия
        if vopr ==1 or vopr == 3:
            for i in range(10):
                pygame.draw.rect(dis, purple, [x_ra[i], y_ra[i], high[i], width[i]])
            for i in kor_prip:    
                if i.collidepoint(x1,y1):
                    game_close=True
        #Проверка на поля
        if (vopr==2 or vopr==3) and game_close!=True:
            game_close=pola(x1,y1)
        elif vopr ==0 or vopr == 1:
            x1,y1=bespola(x1,y1) 

        #Рисует еду, съел еду
        if nachal_dvish == 0:
            circle=pygame.draw.circle(dis, red, (x_rand, y_rand), snake_block)
        if (x1 == x_rand and y1 == y_rand and nachal_dvish==0) or (circle.collidepoint(x1,y1) and nachal_dvish==1):    
            # x_rand, y_rand=na_prepat(kor_prip,dis_width)
            x_rand, y_rand=sov_so_zm(kor_sentr,kor_prip,x1, y1)
            pribav=1
            if nachal_dvish==1:
                time_0_m=time.time()
                rand_vr_m=random.randrange(10, 40, 10)
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




