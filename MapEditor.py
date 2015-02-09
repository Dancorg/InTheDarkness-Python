import pickle
import pygame.key
import pygame.mouse
from pygame.locals import*


ww = 20
hh = 20
cc = 'red'
mat = 0

presets = [(K_1,10,20),(K_2,20,10),(K_3,40,10),(K_4,20,20),(K_5,40,40),(K_6,10,10)]
keys = [K_1,K_2,K_3,K_4,K_5,K_6]

class obs:
    def __init__(self,x,y,w,h,mat):
        self.data = {'x':x,'y':y,'w':w,'h':h,'mat':mat}

class enem:
    def __init__(self,x,y,w,h,c):
        self.data = {'x':x,'y':y,'w':w,'h':h,'color':c}


pygame.init()
size = [800,480] #tamano de la ventana
screen = pygame.display.set_mode(size,pygame.SRCALPHA) #crea una ventana de tamano size
lista = []
lista2 = []
listaE = []
##for i in range(int(size[0]/ww)):
##    lista3 = []
##    for j in range(int(size[1]/hh)):
##        lista3.append(False)
##    lista2.append(lista3)

for i in range(size[0]):
    lista3 = []
    for j in range(size[1]):
        lista3.append(False)
    lista2.append(lista3)

done = False
while not done:
    screen.fill((0,0,0,255))
    mm = pygame.mouse.get_pos()
    pygame.draw.rect(screen,(50,50,50,20),(int(mm[0]/10)*10,int(mm[1]/10)*10,ww,hh),0)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                done = True
        for i in range(len(presets)):
            if pygame.key.get_pressed()[presets[i][0]]:
                print('la')
                ww = presets[i][1]
                hh = presets[i][2]

        if pygame.key.get_pressed()[K_q]:
            cc = 'red'
        if pygame.key.get_pressed()[K_w]:
            cc = 'gray'
        if pygame.key.get_pressed()[K_e]:
            cc = 'black'
        if pygame.key.get_pressed()[K_a]:
            mat = 0
        if pygame.key.get_pressed()[K_s]:
            mat = 1

        if pygame.key.get_pressed()[K_SPACE]:
            ww = int(input("Width: "))
            hh = int(input("Height: "))
        if pygame.mouse.get_pressed()[0] == True:
            xx = int((mm[0])/10)*10#-20
            yy = int((mm[1])/10)*10#-10
##            if lista2[int(xx/ww)-int(ww/2)][int(yy/hh)-int(hh/2)] == False:
##                lista2[int(xx/hh)-int(ww/2)][int(yy/hh)-int(hh/2)] = True
            if lista2[xx][yy] == False:
                lista2[xx][yy] = True
                lista.append(obs(xx,yy,ww,hh,mat))
            else:
                print("no")

        if pygame.mouse.get_pressed()[2] == True:
            xx = int((mm[0])/20)*20#-20
            yy = int((mm[1])/20)*20#-10
            if lista2[xx][yy] == False:
                lista2[xx][yy] = True
                listaE.append(enem(xx,yy,20,20,cc))

        if pygame.mouse.get_pressed()[1] == True:

            for i in lista:
                if mm[0] > i.data['x'] and mm[0] < i.data['x'] + i.data['w'] and mm[1] > i.data['y'] and mm[1] < i.data['y'] + i.data['h']:
                    lista.remove(i)
                    for an in range(i.data['w']):
                        for al in range(i.data['h']):
                            lista2[an+int((mm[0])/i.data['w'])*i.data['w']][al+int((mm[1])/i.data['h'])*i.data['h']] = False
                    print('del')

##            xx = int((mm[0])/ww)*ww#-20
##            yy = int((mm[1])/hh)*hh#-10
##            if lista2[int(xx/ww)-int(ww/2)][int(yy/hh)-int(hh/2)] == True:
##                lista2[int(xx/ww)-int(ww/2)][int(yy/hh)-int(hh/2)] = False
##                for i in lista:
##                    if int(i.data['x']/ww)*ww == xx and int(i.data['y']/hh)*hh == yy:
##                        lista.remove(i)
##                        print('del')
                else:
                    print("no")
    for i in lista:
        if i.data['mat']==0:
            pygame.draw.rect(screen,(150,150,150,255),(i.data['x'],i.data['y'],i.data['w'],i.data['h']),0)
        if i.data['mat']==1:
            pygame.draw.rect(screen,(60,30,10,255),(i.data['x'],i.data['y'],i.data['w'],i.data['h']),0)

    for i in listaE:
        if i.data['color'] == 'red':
            color = (150,20,30,255)
        if i.data['color'] == 'black':
            color = (50,50,50,255)
        if i.data['color'] == 'gray':
            color = (150,150,150,255)

        pygame.draw.rect(screen,color,(i.data['x'],i.data['y'],i.data['w'],i.data['h']),0)

    for w in range(int(size[0]/20)):
        pygame.draw.line(screen,(150,70,90,255),(w*20,0),(w*20,size[1]),1)

    for h in range(int(size[1]/20)):
        pygame.draw.line(screen,(150,70,90,255),(0,h*20),(size[0],h*20),1)

    pygame.display.update()

file = open('map.dat','wb')
pickle.dump(lista,file)
file.close()

file2 = open('map2.dat','wb')
pickle.dump(listaE,file2)
file2.close()

##file = open('map.dat','rb')#.readline()
##b=pickle.load(file)
##print(b)


##for i in range(120): #PLATAFORMAS
##    b = rnd.randrange(0, 800, 40)
##    c = rnd.randrange(50, 460, 20)
##    a = obs(b, c, 40, 20, brown)#buscar una forma de hacer que sea random pero con sentido
##    platforms.append(a)
##    quad.add_obs(a)
##
##for i in range()
