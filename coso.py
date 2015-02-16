import math
from dust import*
from utils import*

class coso:#el jugador
    g = 0
    v = 0
    c = True
    can_jump = True
    can_climb = False
    onwall = False
    illum = True
    onborder = False

    def __init__ (self, surface, x, y, w, h, color, images, size, sounds): #eventualmente iria otra informacion como el color de la linea
        self.sounds = sounds
        self.s = surface
        self.data = {'x':x, 'y':y, 'w':w, 'h':h, 'color':color, 'px':0, 'py':0, 'dir':0, 'borders':[0,0,0,0]}
        self.data['borders'][0] = x - w/2 #left
        self.data['borders'][1] = x + w/2 #right
        self.data['borders'][2] = y - h/2 #top
        self.data['borders'][3] = y + h/2 #bottom
        self.anims = images
        self.size = size
        #self.anim = {'still':brown,'walk':light_blue,'run':blue,'jump':green,'fall':strong_red,'climb':yellow,'throw':white}
        self.anim = {'still':self.anims[0], 'walk':self.anims[2], 'run':self.anims[1], 'jump':self.anims[4], 'fall':self.anims[3], 'climb':self.anims[5], 'throw':self.anims[6]}
        self.cur_anim = self.anim['walk']
        self.anim_support= {'frame':0,'counter':0}

    def get_pos(self):
        return (self.data['x'], self.data['y'])

    def get_pos_size(self):
        return (self.data['x'] - self.data['w']/2, self.data['y'] - self.data['h']/2, self.data['w'], self.data['h'])

    def get_pos_size_prev(self):
        return (self.data['px'] - self.data['w']/2, self.data['py'] - self.data['h']/2, self.data['w'], self.data['h'])

    def set_pos(self, x, y):
        #self.data = {'x':x,'y':y}#en el caso de que tenga que agregar mas datos seria mas conveniente usar el metodo tradicional de abajo
        self.data['x'] = x
        self.data['y'] = y

    def check_col(self, p):#p es la lista de obstaculos
        for i in p:
            if self.data['x'] in range(i.data['x'], i.data['x'] + i.data['w']) and self.data['y'] in range(i.data['y'], i.data['y'] + i.data['h']):
                return True
            else:
                return False

    def check_pos(self, x, y, p):#similar a check_col, pero en vez de tomar su propia posicion deberia tomar una posicion dada por parametro, para poder ver si esa posicion esta libre para moverse
        for i in p:
            if x in range(int(i.data['x'] - i.data['w']/2), int(i.data['x'] + i.data['w']/2)) and y in range(int(i.data['y'] - i.data['h']/2), int(i.data['y'] + i.data['h']/2)):
                #print('True')
                return i
            else:
                #print('False')
                a = None
        return a

    def check_pos_specific(self, x, y, p):#specific es que en vez de dar una lista de obstaculos da la id de un obstaculo especifico
        if x in range(p.data['x'], p.data['x'] + p.data['w']) and y in range(p.data['y'], p.data['y'] + p.data['h']):
            return True
        else:
            return False

    def check_area(self, x, y, w, h, p):#area rectangular con centro en (x,y)
        Al = x - w/2 #left
        Ar = x + w/2 #right
        At = y - h/2 #top
        Ab = y + h/2 #bottom

        for i in p:
            Bl = i.data['x'] - i.data['w']/2
            Br = i.data['x'] + i.data['w']/2
            Bt = i.data['y'] - i.data['h']/2
            Bb = i.data['y'] + i.data['h']/2

            if Al < Br and Ar > Bl and At < Bb and Ab > Bt :
                #print('lol')
                return i #podria devolver una lista [True,i] para usar tanto el bool como la instancia
        return None

    def check_area_specific(self, x, y, w, h, p):#specific es que en vez de dar una lista de obstaculos da la id de un obstaculo especifico
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

    def move(self, dir, cant, p, grav=False):#move se usa tanto para el movimiento por teclas como para el mov por gravedad (cuando grav==True)
        b = None
        self.c = True
        self.onwall = False

        a = [0,0,0,0] #en vez de hacer 4 variables hago un array
        a[0] = math.cos(dir) #convierte el angulo en componentes de un vector
        a[1] = math.sin(dir)
        a[2] = a[0]*(cant) #multiplico el vector por la velocidad
        a[3] = a[1]*(cant)

        if cant > self.data['h']:
            b = self.check_area(self.data['x'] + a[2], self.data['y'] + self.data['h'], self.data['w'], self.data['h'], p)
        if b == None:
            b = self.check_area(self.data['x'] + a[2], self.data['y'] + a[3], self.data['w'], self.data['h'], p) #chequea si cuando se mueva chocaria contra una pared

        if b == None or self.can_climb:
            #no hay obstaculos, puede moverse
            self.data['x'] += a[0]*cant #si, podria usar a[2] y a[3] pero quizas meto otro factor que lo haga diferente
            self.data['y'] += a[1]*cant
        else: #hay un obstaculo
            if grav: #si el metodo fue llamado desde la funcion gravity
                if self.g > 0: #si la caja esta subiendo
                    if self.g > 7:
                        self.sounds.stop()
                        self.sounds.set_volume(1)
                        self.sounds.play()
                        self.ruido = True
                    elif self.g >1:
                        self.sounds.stop()
                        self.sounds.set_volume(0.4)
                        self.sounds.play()
                    self.g = 0 #deja de subir, lol
                    self.can_jump = True
                    self.move_to_contact(math.radians(90),1,b) #se mueve solo hasta tocar el obstaculo
                else:
                    self.g = 0 #si la caja esta cayendo, lo mismo
                    self.move_to_contact(math.radians(270),1,b)
            else:
                #if self.g > 0:
                self.check_wall(p)
                self.move_to_contact(dir,1,b) #si la funcion fue llamada por el movimiento del jugador, se mueve solo hasta tocar el obstaculo

        if(self.data['y']>self.size[1]):#or self.data['y']<0 no quiero que muera si salta
            self.set_pos(20,0)
            self.g = 0
            cant = 0
        #pygame.draw.rect(screen,self.data['color'],self.get_pos_size_prev(),0)
        #prev=self.get_pos_size_prev()

        #print(self.v, grav)
        if grav == True: #no tiene sentido ahora (antes tampoco, pero funcionaba :P)
            self.v = (math.fabs(self.data['y'] - self.data['py']))
            self.data['px'] = self.data['x']
            self.data['py'] = self.data['y']
        #return prev
        if not grav:
            if self.onwall:
                self.cur_anim = self.cycle_anim(self.anim['climb'],10)#self.anim['climb'][0]
            else:
                if self.g > 1:
                    self.can_jump = False
                if self.can_jump:
                    if cant <= 0:
                        self.cur_anim = self.cycle_anim(self.anim['still'],2) #self.anim['still'][0]
                    elif cant <= 1:
                        self.cur_anim = self.cycle_anim(self.anim['walk'],3) #self.anim['walk'][0]
                    elif cant > 1:
                        self.cur_anim = self.cycle_anim(self.anim['run'],1) #self.anim['run'][1]
                else:
                    if self.g > 0:
                        self.cur_anim = self.cycle_anim(self.anim['jump'],2) #self.anim['jump'][0]
                    else:
                        self.cur_anim = self.cycle_anim(self.anim['fall'],2) #self.anim['fall'][0]
        self.can_climb = False

    def move_to_contact(self, dir, cant, b): #reemplazar dir por la direccion real
        a=[self.data['x'],self.data['y'],self.data['x'],self.data['y']]
        while not self.check_area_specific(a[0],a[1],self.data['w'],self.data['h'],b):
            a[2] = a[0]
            a[3] = a[1]
            a[0] += math.cos(dir)
            a[1] += math.sin(dir)
        self.set_pos(a[2],a[3])


    def gravity(self,p):
        #a=self.data['size']+5
        if self.onborder == False:
            self.g += 1
        self.onborder = False
        self.move(math.radians(90), self.g, p, True)

    def jump(self,cant,p):
        #print(self.g)
        #if self.g==1:
        if self.can_jump:
            self.move(math.radians(90), cant, p)
            self.can_jump = False
            self.g =- cant

    def throw_dust(self, lights, dire, cant, am, t=None):
        a = dust(self.s, self.data['x'], self.data['y'], white, am, am, dire, cant, self.g, t)
        lights.append(a)

    def check_wall(self, p):
        self.can_climb = False
        mm = 0
        a = self.check_pos(int(self.data['x'] - self.data['w']/2-1), int(self.data['y'] - self.data['h']/2), p)
        b = self.check_pos(int(self.data['x'] + self.data['w']/2+1), int(self.data['y'] - self.data['h']/2), p)
        if a != None:
            mm = a.data['material']
        if b != None:
            mm = b.data['material']
        if mm == 1 or (a == None and b == None): #si el material == 1 entonces la pared es escalable
            self.onwall = True
            if self.g > 0:
                self.g -= 1
            if mm == 1 and (a != None or b != None): #si la pared es escalable y esta lejos del borde
                self.can_climb = True
                self.can_jump = True #Temporal hasta que haga funcionar el climb :/
            else:
                self.can_jump = True
                self.onborder = True
        else:
            if self.g > 0:
                self.g -= 0.5
            self.onwall = False

    def cycle_anim(self,anim,dur):
        #counter = self.anim_support['counter']
        #a = self.anim_support['frame']
        self.ruido = False
        if (self.cur_anim == self.anim['walk'][2] or self.cur_anim == self.anim['walk'][5]) and self.anim_support['counter'] == 0:
            self.sounds.stop()
            self.sounds.set_volume(0.3)
            self.sounds.play()
        if (self.cur_anim == self.anim['run'][2] or self.cur_anim==self.anim['run'][5]) and self.anim_support['counter'] == 0:
            self.sounds.stop()
            self.sounds.set_volume(0.7)
            self.sounds.play()
            self.ruido = True
        if  self.anim_support['counter'] == 0:
            self.anim_support['counter'] = dur
            self.anim_support['frame'] += 1
            if self.anim_support['frame'] == 6:
                self.anim_support['frame'] = 0
        else:
            self.anim_support['counter'] -= 1
        return anim[self.anim_support['frame'] - 1]

