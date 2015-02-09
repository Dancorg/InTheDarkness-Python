import math

class spark:

    def __init__(self,x,y):
        self.data = {'x': x, 'y': y, 'cant': 0}
        self.dir = 0
        self.cant = rnd.randrange(-6, 6)
        self.time = rnd.randrange(3, 7)
        self.g = rnd.randrange(-6, 4)

    def gravity(self):
        self.move(math.radians(90),self.g)
        self.g += 1

    def move(self,dir,cant):
        a = [0,0,0,0] #en vez de hacer 4 variables hago un array

        a[0] = math.cos(dir) #convierte el angulo en componentes de un vector
        a[1] = math.sin(dir)
        a[2] = a[0]*(cant) #multiplico el vector por la velocidad
        a[3] = a[1]*(cant)

        self.data['x'] += a[2]
        self.data['y'] += a[3]

    def update(self,px,c):
        self.gravity()
        self.move(self.dir, self.cant)
        self.time -= 1
        xx = int(self.data['x'])
        yy = int(self.data['y'])
        if xx>0 and xx<size[0] and yy>0 and yy< size[1]:
            px[xx][yy] = (255,255,255,255)
        if self.time <= 0:
            c.remove(self)

