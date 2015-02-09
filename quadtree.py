import pygame
import math

class quadtree:

    def __init__(self,x,y,w,h, level):
        self.isleaf = False
        self.child = []
        self.pos = [0,0,0,0]# x y w h

        self.pos[0] = x
        self.pos[1] = y
        self.pos[2] = w
        self.pos[3] = h

        #if level == 2: self.draw()

        self.level = level
        level += 1
        if level <= 3: #cambiar por una variable global
            self.child.append(quadtree(x, y, w/2, h/2,level))#arriba izquierda
            self.child.append(quadtree(x+w/2, y, w/2, h/2,level))#arriba derecha
            self.child.append(quadtree(x, y+h/2, w/2, h/2,level))#abajo izquierda
            self.child.append(quadtree(x+w/2, y+h/2, w/2, h/2,level))#abajo derecha
        else:
            self.isleaf = True # es la subdivision mas chica
            #leaves = [] # lista de los objetos dentro de la division
        #print(self.level,self.isleaf,len(self.child))

    def draw(self,color):
        pygame.draw.rect(s, color, (self.pos[0],self.pos[1],self.pos[2], self.pos[3]), 1)

    def get_pos_size(self):
        return (self.pos[0],self.pos[1],self.pos[2],self.pos[3])

    def check_area_specific(self,size,p):#specific es que en vez de dar una lista de obstaculos da la id de un obstaculo especifico
        pp = p.data
        Al = size[0] #left
        Ar = size[0] + size[2] #right
        At = size[1] #top
        Ab = size[1] + size[3] #bottom

        Bl = pp['x'] - pp['w']/2
        Br = pp['x'] + pp['w']/2
        Bt = pp['y'] - pp['h']/2
        Bb = pp['y'] + pp['h']/2

        if Al < Br and Ar > Bl and At < Bb and Ab > Bt :
            return p #podria devolver una lista [True,i] para usar tanto el bool como la instancia
        else:
            return None

    def add_obs(self,obs): #busca en que leaf tiene que estar el obs y lo guarda
        #o = obs.get_pos_size()

        def loop(self,obs):
            ch = self.child

            if self.isleaf:
                if self.check_area_specific(self.get_pos_size(),obs) != None:
                    #self.draw(white)
                    ch.append(obs)
                    #print(len(ch))
            else:
                for i in ch:
                    loop(i,obs)

        loop(self,obs)

    def retrieve(self,l):
        lista = []

        def loop(self,obs,lista):
            for i in self.child:
                if i.check_area_specific(i.get_pos_size(),obs) != None:
                    if i.isleaf:
                        i.draw(red)
                        lista += i.child
                    else:
                        loop(i,obs,lista)
        loop(self,l,lista)
        #print(len(lista))
        return lista
