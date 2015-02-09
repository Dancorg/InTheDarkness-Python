import math
import pygame
from utils import*

class dust:
    def __init__(self, x, y, color, time, intensity, direction, cant, g, tipo = None, static = False):
        self.tipo = tipo
        self.chispita = []
        self.g = g - 8 #para que aparezca saltando
        self.data = {'x':x,'y':y,'w':intensity,'h':intensity,'color':color,
                   'time':time, 'state':0,'intensity':intensity,
                   'dir':math.radians(direction),'cant':math.fabs(cant),
                   'borders':[0,0,0,0], 'static':static}# w y h son para poder hacer el line of sight
        ii = intensity/2
        self.data['borders'][0] = x-ii #left
        self.data['borders'][1] = x+ii #right
        self.data['borders'][2] = y-ii #top
        self.data['borders'][3] = y+ii #bottom
        self.ll = []

    def update(self,p,l):
        if not self.data['static']:
            if ang == 0: #segun para que lado este mirando el jugador
                cc = 1
            else:
                cc = -1
            if self.data['time'] > 0:
                self.data['time'] -= 1 #timer
                self.data['intensity'] -= 1 #size

                if self.tipo == None: #depende el modo de la luz, se mueve o queda fija
                    self.gravity(p)
                    self.move(self.data['dir'], self.data['cant']*1.5, p)
                else:
                    self.data['x'] = self.tipo.data['x'] + cc*5
                    self.data['y'] = self.tipo.data['y'] - 8
            else:
                l.remove(self) #se destruye

    def check_pos(self, x, y, p):#similar a check_col, pero en vez de tomar su propia posicion deberia tomar una posicion dada por parametro, para poder ver si esa posicion esta libre para moverse
        for i in p:
            if x in range(i.data['x'], i.data['x'] + i.data['w']) and y in range(i.data['y'], i.data['y'] + i.data['h']):
                #print('True')
                return i
            else:
                #print('False')
                return None

    def check_pos_specific(self,x,y,p):#specific es que en vez de dar una lista de obstaculos da la id de un obstaculo especifico
        if x in range(p.data['x'], p.data['x'] + p.data['w']) and y in range(p.data['y'], p.data['y'] + p.data['h']):
            return p
        else:
            return None


    def get_pos_size(self):
        return (self.data['x']-self.data['intensity']/2,self.data['y']-self.data['intensity']/2,self.data['intensity'],self.data['intensity'])

    def gravity(self,p):
        self.move(math.radians(90), self.g, p, True)
        self.g += 1
        if self.g > 1 or self.g < 0:
            self.contact = False

    def move_to_contact(self,dir,cant,b): #reemplazar dir por la direccion real
        a = [self.data['x'],self.data['y'],self.data['x'],self.data['y']]
        #print(a[0],a[1],b)
        while not self.check_pos_specific(a[0],a[1],b):
            a[2] = a[0]
            a[3] = a[1]
            a[0] += math.cos(dir)
            a[1] += math.sin(dir)
        self.data['x'] = a[2]
        self.data['y'] = a[3]

    def move(self,dir,cant,p,grav=False):
        b=None
        a = [0,0,0,0] #en vez de hacer 4 variables hago un array

        a[0] = math.cos(dir) #convierte el angulo en componentes de un vector
        a[1] = math.sin(dir)
        a[2] = a[0]*(cant) #multiplico el vector por la velocidad
        a[3] = a[1]*(cant)
        b = scanOtroMas((self.data['x'],self.data['y']),(self.data['x']+a[2],self.data['y']+a[3]),50,p)[0]
        if b != None:
            if math.fabs(self.data['cant']) > 0:
                self.data['cant'] -= 1
            #pygame.draw.rect(screen,red,b.get_pos_size(),0)
        if b == None:
            self.data['x'] +=a [2]
            self.data['y'] +=a [3]
        else:
            if grav: #si el metodo fue llamado desde la funcion gravity
                if self.g > 0: #si la caja esta subiendo
                    self.g = 0 #deja de subir, lol
              #      self.move_to_contact(math.radians(90),1,b) #se mueve solo hasta tocar el obstaculo
                else:
                    self.g = 0 #si la caja esta cayendo, lo mismo
        if grav == True: #no tiene sentido ahora (antes tampoco, pero funcionaba :P)
            self.data['px'] = self.data['x']
            self.data['py'] = self.data['y']
    #def illum(self,px,pxl):

    def plotCircle(self, x0, y0, radius,qual,lll):
        x0 = int(x0)
        y0 = int(y0)
        radius = int(radius*qual)
        f = 1 - radius
        ddF_x = qual
        ddF_y = -2 * radius
        x = 0
        y = radius

        b = scanOtroMas((x0,y0 + radius),(x0,y0),radius+qual,lll)
        if b[0] != None:
            self.line(x0, y0, b[1], b[2], qual)
        else:
            self.line(x0, y0, x0, y0 + radius, qual)

        b = scanOtroMas((x0,y0 - radius),(x0,y0),radius+qual,lll)
        if b[0] != None:
            self.line(x0, y0, b[1], b[2], qual)
        else:
            self.line(x0, y0, x0, y0 - radius, qual)

        b = scanOtroMas((x0 + radius,y0 ),(x0,y0),radius+qual,lll)
        if b[0] != None:
            self.line(x0, y0, b[1], b[2], qual)
        else:
            self.line(x0, y0, x0 + radius, y0, qual)

        b = scanOtroMas((x0 - radius,y0 ),(x0,y0),radius+qual,lll)
        if b[0] != None:
            self.line(x0, y0, b[1], b[2], qual)
        else:
            self.line(x0, y0, x0 - radius, y0, qual)

        while(x < y):

            # ddF_x == 2 * x + 1;
            # ddF_y == -2 * y;
            # f == x*x + y*y - radius*radius + 2*x - y + 1;
            if(f >= 0):
                y -= qual
                ddF_y += 2*qual
                f += ddF_y
            x+= qual
            ddF_x += 2*qual
            f += ddF_x
            xax = x0 +x ; xbx = x0 -x ; yay = y0 +y ; yby = y0 -y
            xay = x0 +y ; xby = x0 -y ; yax = y0 +x ; ybx = y0 -x

            b = scanOtroMas((xax,yay),(x0,y0),radius+qual,lll)
            if b[0] != None:
                self.line(x0, y0, b[1], b[2], qual)
            else:
                self.line(x0, y0, xax, yay, qual)

            b = scanOtroMas((xbx,yay),(x0,y0),radius+qual,lll)
            if b[0] != None:
                self.line(x0, y0, b[1], b[2], qual)
            else:
                self.line(x0, y0, xbx, yay, qual)

            b = scanOtroMas((xax,yby),(x0,y0),radius+qual,lll)
            if b[0] != None:
                self.line(x0, y0, b[1], b[2], qual)
            else:
                self.line(x0, y0, xax, yby, qual)

            b = scanOtroMas((xbx,yby),(x0,y0),radius+qual,lll)
            if b[0] != None:
                self.line(x0, y0, b[1], b[2], qual)
            else:
                self.line(x0, y0, xbx, yby, qual)

            b = scanOtroMas((xay,yax),(x0,y0),radius+qual,lll)
            if b[0] != None:
                self.line(x0, y0, b[1], b[2], qual)
            else:
                self.line(x0, y0, xay, yax, qual)

            b = scanOtroMas((xby,yax),(x0,y0),radius+qual,lll)
            if b[0] != None:
                self.line(x0, y0, b[1], b[2], qual)
            else:
                self.line(x0, y0, xby, yax, qual)

            b = scanOtroMas((xay,ybx),(x0,y0),radius+qual,lll)
            if b[0] != None:
                self.line(x0, y0, b[1], b[2], qual)
            else:
                self.line(x0, y0, xay, ybx, qual)

            b = scanOtroMas((xby,ybx),(x0,y0),radius+qual,lll)
            if b[0] != None:
                self.line(x0, y0, b[1], b[2], qual)
            else:
                self.line(x0, y0, xby, ybx, qual)

    def line(self, x1, y1, x0, y0,qual):
        pygame.draw.line(self.s,(0,0,0,120),(x0,y0),(x1,y1),8)
        pygame.draw.circle(self.s,(0,0,0,120),(int(x0),int(y0)),qual,0)
