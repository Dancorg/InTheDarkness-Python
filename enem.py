import math
from alt_target import*
from utils import*

class enem:
    illum = False
    g = 0
    cant = 0
    contact = False
    chase_timer = 1
    seg = False
    blinded = False
    volume = 0

    def __init__(self,x,y,w,h,color,speed,a,images,size,material=0):
        self.data={'x':x,'y':y,'w':w,'h':h,'color':color,'speed':speed,'st':(x,y),'type':a,'borders':[0,0,0,0],'material':material}
        self.data['borders'][0] = x - w/2 #left
        self.data['borders'][1] = x + w/2 #right
        self.data['borders'][2] = y - h/2 #top
        self.data['borders'][3] = y + h/2 #bottom
        self.alt_t = alt_target(self,x,y,w,h)
        self.alert = 30
        self.size = size
        anims = images
        self.anim = {'still':anims[0],'walk':anims[2],'run':anims[1],'jump':anims[4],'fall':anims[3],'climb':anims[5],'throw':anims[6]}
        self.cur_anim = self.anim['walk'][0]
        self.anim_support= {'frame':0,'counter':0}

    def get_pos(self):
        return (self.data['x'],self.data['y'])

    def get_pos_size(self):
        return (self.data['x']-self.data['w']/2,self.data['y']-self.data['h']/2,self.data['w'],self.data['h'])

    def set_pos(self,x,y):
        self.data['x'] = x
        self.data['y'] = y

    def get_color(self):
        return self.data['color']

    def check_pos(self,x,y,p):#similar a check_col, pero en vez de tomar su propia posicion deberia tomar una posicion dada por parametro, para poder ver si esa posicion esta libre para moverse
#        for i in p:
#            if x in range(int(i.data['x']-i.data['w']/2),int(i.data['x']+i.data['w'])) and y in range(int(i.data['y']-i.data['h']/2),int(i.data['y']+i.data['h'])):
#                #print('True')
#                return i
#        return None
        if obs_map[int(x/10)][int(y/10)][0] == True:
            return obs_map[int(x/10)][int(y/10)][1]
        else:
            return None

    def check_area(self,x,y,w,h,p):#area de centro (x,y) y radio s vs area de 'p'
        Al = x - w/2 #left
        Ar = x + w/2 #right
        At = y - h/2 #top
        Ab = y + h/2 #bottom

        for i in p:
            Bl = i.data['x'] - i.data['w']/2
            Br = i.data['x'] + i.data['w']/2
            Bt = i.data['y'] - i.data['h']/2
            Bb = i.data['y'] + i.data['h']/2

            if Al < Br and Ar > Bl and At < Bb and Ab > Bt:
                #print('lol')
                return i #podria devolver una lista [True,i] para usar tanto el bool como la instancia
        return None

    def check_area_specific(self,x,y,w,h,p):#specific es que en vez de dar una lista de obstaculos da la id de un obstaculo especifico
        Al = x - w/2 #left
        Ar = x + w/2 #right
        At = y - h/2 #top
        Ab = y + h/2 #bottom

        Bl = p.data['x'] - p.data['w']/2
        Br = p.data['x'] + p.data['w']/2
        Bt = p.data['y'] - p.data['h']/2
        Bb = p.data['y'] + p.data['h']/2

        if Al < Br and Ar > Bl and At < Bb and Ab > Bt :
            return p #podria devolver una lista [True,i] para usar tanto el bool como la instancia
        else:
            return None

    def move(self,dir,cant,p,grav=False):
        b=None
        a = [0,0,0,0] #en vez de hacer 4 variables hago un array

        a[0] = math.cos(dir) #convierte el angulo en componentes de un vector
        a[1] = math.sin(dir)
        a[2] = a[0]*(cant) #multiplico el vector por la velocidad
        a[3] = a[1]*(cant)

        if cant > self.data['h']:
            b = self.check_area(self.data['x']+a[2],self.data['y']+self.data['h'],self.data['w'],self.data['h'],p)

        if b == None:
            b = self.check_area(self.data['x']+a[2],self.data['y']+a[3],self.data['w'],self.data['h'],p)
            #pygame.draw.rect(screen,(255,0,0),(self.data['x']+a[2],self.data['y']+a[3],self.data['w'],self.data['h']),1)

        if b == None:
            self.data['x'] += a[2]
            self.data['y'] += a[3]
        else:
            if grav: #si el metodo fue llamado desde la funcion gravity
                if self.g > 0: #si la caja esta subiendo
                    if self.g > 1:
                        snd_step2.stop()
                        snd_step2.set_volume(self.volume)
                        snd_step2.play()

                if self.g > 0: #si la caja esta subiendo
                    self.g = 0 #deja de subir, lol
                    self.move_to_contact(math.radians(90),1,b) #se mueve solo hasta tocar el obstaculo
                else:
                    self.g = 0 #si la caja esta cayendo, lo mismo
                    self.move_to_contact(math.radians(270),1,b)
            else:
                self.move_to_contact(dir,1,b) #si la funcion fue llamada por el movimiento del jugador, se mueve solo hasta tocar el obstaculo
            if b.__class__.__name__ == 'coso' and not self.blinded: #Cuando mata al jugador
                        b.set_pos(20,0)
                        b.g = 0
                        cant = 0

        if(self.data['x']<0 or self.data['x']>self.size[0]  or self.data['y']>self.size[1]):#or self.data['y']<0
            self.set_pos(self.data['st'][0],self.data['st'][1])
            self.g = 0
            self.cant = 0

        if grav == True: #no tiene sentido ahora (antes tampoco, pero funcionaba :P)
            self.data['px'] = self.data['x']
            self.data['py'] = self.data['y']


        if not grav:
##            if self.onwall:
##                self.cur_anim = self.cycle_anim(self.anim['climb'],10)#self.anim['climb'][0]
##            else:
                if self.g == 1:
                    if cant == 0:
                        self.cur_anim = self.cycle_anim(self.anim['still'],2) #self.anim['still'][0]
                    elif cant <= 1:
                        self.cur_anim = self.cycle_anim(self.anim['run'],2) #self.anim['walk'][0]
                    elif cant > 1:
                        self.cur_anim = self.cycle_anim(self.anim['run'],1) #self.anim['run'][1]
                else:
                    if self.g > 1:
                        self.cur_anim = self.cycle_anim(self.anim['jump'],2) #self.anim['jump'][0]
                    elif self.g < 0:
                        self.cur_anim = self.cycle_anim(self.anim['fall'],2) #self.anim['fall'][0]
        #print(math.degrees(dir))
#        if math.degrees(dir) == 180:
#            #print(self.cur_anim)
#            self.cur_anim = pygame.transform.flip(self.cur_anim,True,False)
#        else:
#            self.cur_anim = pygame.transform.flip(self.cur_anim,True,False)

    def move_to_contact(self,dir,cant,b): #
        a = [self.data['x'],self.data['y'],self.data['x'],self.data['y']]
        while not self.check_area_specific(a[0],a[1],self.data['w'],self.data['h'],b):
            a[2] = a[0]
            a[3] = a[1]
            a[0] += math.cos(dir)
            a[1] += math.sin(dir)
        self.set_pos(a[2],a[3])
        #print(a[2],a[3])
        if dir != math.radians(270):
            self.contact = True

    def check_fall(self,dir,p):
        a = math.cos(math.radians(dir))
        #print(a)
        if (self.check_area(self.data['x']+self.data['w']*(a-1/2),self.data['y']
            +self.data['h']/2,self.data['w'],self.data['h'],p)) != None:
            #pygame.draw.rect(screen,(250,0,0,200),(self.data['x']+self.data['w']*(a-1/2),self.data['y']+self.data['h']/2,self.data['w'],self.data['h']),1)
            #si hay un obstaculo(plataforma o jugador)
            return False
        else: #y digo yo, no se, digo, no sera mas rapido checkear solo un punto en vez de el area entera?????

            return True

    def check_wall(self,dir,p):
        a = math.cos(math.radians(dir))
        if (self.check_area(self.data['x']+self.data['w']*(a-1/2),
            self.data['y'],self.data['w'],self.data['h'],p)) != None:
            #si hay un obstaculo(plataforma o jugador)
            return False
        else:
            return True

    def gravity(self,p):
        self.move(math.radians(90),self.g,p,True)
        self.g += 1
        if self.g > 1 or self.g < 0:
            self.contact = False

    def jump(self,cant,p):
        a = self.check_pos(int(self.data['x']-self.data['w']/2),int(10 + self.data['y']+self.data['h']/2),p)
        b = self.check_pos(int(self.data['x']+self.data['w']/2),int(10 + self.data['y']+self.data['h']/2),p)
        if self.g == 1  and (a != None or b != None):
            self.move(math.radians(90),cant,p)
            self.g -= cant

    def ojitos(self,l,p,t,px):
        dmin = 100
        if self.dir == 0:
            c = [-3,2]
        else:
            c = [-8,-3]
        if self.data['type'] == 1:
            for i in l:
                a = point_distance(i,self)
                if a < dmin:# and scan(self,i,p):
                    if scan(self,i,p):
                        dmin = a
                        b = int(255 - a*2)#int(255*(i.data['intensity']/100))#

                        if (self.data['x']>0 and self.data['x'] < self.size[0] and
                            self.data['y']>0 and self.data['y'] < self.size[1]):
                            px[int(self.data['x'] + c[0])][int(self.data['y'] - 3)] = (b, b, b, 255)
                            px[int(self.data['x'] + c[1])][int(self.data['y'] - 3)] = (b, b, b, 255)

        if self.data['type'] == 0:
            a = point_distance(t,self)
            if scan(self,t,p):
                if self.data['x']>0 and self.data['x'] < self.size[0] and self.data['y']>0 and self.data['y']< self.size[1]:
                    px [int(self.data['x'] + c[0])][int(self.data['y'] - 3)] = (150, 10, 20, 255)
                    px [int(self.data['x'] + c[1])][int(self.data['y'] - 3)] = (150, 10, 20, 255)

    def behave_simple(self,t,p):
        pd = point_distance(t,self)
        pf = 1 - pd/300
        self.volume = pf if pd <=300 else 0
        vel = self.data['speed']
        self.dir = 0
        if self.data['type'] == 0:
            cc = self.illum
            if cc == True:
                self.seg = False
                self.blinded = True
                self.chase_timer = 50 #tiempo de ceguera
        if self.data['type'] == 1:
            if  t.illum or (t.ruido and pd < 200):
                cc = False
            else:
                cc = True

        self.chase_timer -= 1
        if self.chase_timer <= 0:
            self.blinded = False
            self.alert -= 1
            if scan(self,t,p) and (cc == False or pd < self.data['w']+2):
                self.seg = True
                #self.alt_t.update(t)
                if t != self.alt_t:
                    self.alert = 10 #durante cuanto tiempo persigue al jugador despues de perderlo de vista
            else:
                self.seg = False
            self.chase_timer = 10 #cada cuanto se fija si esta viendo al jugador
        if self.seg == False:
            t = self.alt_t
        if self.alert <= 0:
            self.alt_t.return_to_owner()
        #print(self.alt_t == t, self.alert)
        self.alt_t.update(t)

        if math.fabs(self.alt_t.data['x']-self.data['x'])<=self.data['w']+3:
            #self.alt_t.return_to_owner()
            self.chase_timer=0

        if not self.blinded and (self.seg or (t == self.alt_t and self.alert > 0)) :#buscar la forma de no llamarlo en cada ciclo
            if(t.data['x'] < self.data['x']) and math.fabs(t.data['x']-self.data['x'])>1:
                self.dir = 180
                if self.cant > 0: self.dir = 0
                if self.cant >- vel: self.cant -= 1
            if(t.data['x'] > self.data['x'])and math.fabs(t.data['x']-self.data['x'])>1:
                self.dir = 0
                if self.cant < 0: self.dir = 180
                if self.cant < vel: self.cant += 1
            if self.data['y'] > t.data['y'] and self.contact == True: #si el jugador esta arriba
                num = math.fabs(t.data['y'] - self.data['y'])
                if num != 0:
                    if math.fabs(t.data['x'] - self.data['x'])/math.fabs(num) < 1 : #si el jugador esta a mas de 45grados
                        self.jump(1 + vel*2, p + [t])
            if (self.check_fall(self.dir,p) or not self.check_wall(self.dir,p) )and self.contact == True:
                if t.data['y'] > self.data['y']: #si el jugador esta debajo
                    if math.fabs(t.data['x']-self.data['x'])/math.fabs(t.data['y']-self.data['y']) < 1: #si el jugador esta a mas de 45grados
                        self.jump(1 + vel*2, p + [t])
                else:
                    self.jump(1 + vel*2, p + [t])
        else:
            if self.cant > 0:
                self.cant -= 1
            if self.cant < 0:
                self.cant += 1
        if self.cant != 0:
            self.move(math.radians(self.dir), math.fabs(self.cant), p+[t])

##        else:
##            self.jump(2,p+[t])

    def cycle_anim(self,anim,dur):
        #counter = self.anim_support['counter']
        #a = self.anim_support['frame']
        if (self.cur_anim==self.anim['walk'][2] or self.cur_anim==self.anim['walk'][5] or self.cur_anim==self.anim['run'][2] or self.cur_anim==self.anim['run'][5]) and self.anim_support['counter'] == 0:
            snd_step2.stop()
            snd_step2.set_volume(self.volume)
            snd_step2.play()
        if  self.anim_support['counter'] == 0:
            self.anim_support['counter'] = dur
            self.anim_support['frame'] += 1
            if self.anim_support['frame'] == 6:
                self.anim_support['frame'] = 0
        else:
            self.anim_support['counter'] -= 1
        #print(anim[self.anim_support['frame']-1])
        return anim[self.anim_support['frame']-1]

