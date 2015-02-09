import math

def scan_grid( x1, y1, x0, y0,qual,grid,tipos = []): #DEPRECATED?
    x0 = int(x0)
    x1 = int(x1)
    y0 = int(y0)
    y1 = int(y1)
    dx =  int(math.fabs(x1-x0))
    sx = 1 if x0<x1 else -1
    dy = -int(math.fabs(y1-y0))
    sy = 1 if y0<y1 else -1
    err = dx+dy
    #e2 /* error value e_xy */
    c = 0
    while(True):  #/* loop */
        c += 1
        print(x0,x1)
        if grid[int(x0/10)][int(x1/10)][0]==True:
            return (grid[int(x0/10)][int(x1/10)][1],x0,x1)
            break
        pygame.draw.circle(screen,(0,0,255,120),(x0,y0),2,0)
        if (x0 == x1 and y0 == y1):
            break
        e2 = 2*err
        if (e2 >= dy):
            err += dy; x0 += sx #/* e_xy+e_x > 0 */
        if (e2 <= dx):
            err += dx; y0 += sy #/* e_xy+e_y < 0 */
    return [None]

def point_distance(p1,p2):
    return math.sqrt((p1.data['x']-p2.data['x'])**2 + (p1.data['y']-p2.data['y'])**2)

def point_distanceB(p1,p2):#puntos en vez de objetos
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def fast_point_distance(p1,p2):
    return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 #no da la distancia real, pero sirve para hacer comparaciones (no esta probada todavia)

def is_blocked(a,x,y):
    pp = (int(x/10),int(y/10))
    ss == a[pp[0]][pp[1]]
    if ss == True:
        return ss[1]
    else:
        return None

def scan(s,t,p,typ=True): #linea de vision: muchas cosas feas de algebra
    #return True
    r = True
    if typ:
        a1 = [s.data['x'], s.data['y']]
        a2 = [t.data['x'], t.data['y']]
    else:
        a1 = [s[0], s[1]]
        a2 = [t[0], t[1]]
    dis1 = fast_point_distance(a1,a2)

    def scanB(dat1,dat2,dat3,dat4): #funcion dentro de otra funcion, funception :D
        den = ((dat4[1]-dat3[1])*(dat2[0]-dat1[0]))-((dat4[0]-dat3[0])*(dat2[1]-dat1[1]))
        if den == 0:
            return False #None
        else:
            ua = (((dat4[0]-dat3[0]) * (dat1[1]-dat3[1])) - ((dat4[1]-dat3[1]) * (dat1[0]-dat3[0])))/den
            ub = (((dat2[0]-dat1[0]) * (dat1[1]-dat3[1])) - ((dat2[1]-dat1[1]) * (dat1[0]-dat3[0])))/den

            if (ua<0)or(ua>1)or(ub<0)or(ub>1):
                return False#no colision
            else:
                return True#si colision

    for i in p: # la idea es representar cada plataforma como 2 lineas cruzadas diagonales en vez de chequear cada segmento por separado
        dis2 = fast_point_distance(a1,(i.data['x'],i.data['y']))
        iix = i.data['x']
        iiy = i.data['y']
        ww = i.data['w']/2
        hh = i.data['h']/2
        if dis2 < dis1:
            b1 = [iix - ww, iiy - hh] #\
            b2 = [iix + ww, iiy + hh]

            c1 = [iix - ww, iiy + hh]#/
            c2 = [iix + ww, iiy - hh]

            if not scanB(a1,a2,b1,b2) and not scanB(a1,a2,c1,c2):
                if typ: # typ es usado por la clase dust, que en vez de chequear un area de colision chequea una linea, por eso necesita devolver el objeto y no un un bool
                    r = True
                else:
                    r = None
            else:
                if typ:
                    return False
                else:
                    return i
        if typ:
            r = True
        else:
            r = None
    return r

def scanOtro(a1,a2,dd,p): #tiene que tomar, distancia , punto origen, punto final, obstaculos. tiene que devolver el punto de contacto
    #return True
    r = None

    def scanC(dat1,dat2,dat3,dat4): #funcion dentro de otra funcion, funception :D
        #s = [dat4[0]-dat3[0], dat4[1] - dat3[1], dat2[1]-dat1[1], dat2[0]-dat1[0], dat1[1] - dat3[1], dat1[0] - dat3[0]]
        s0 = dat4[0] - dat3[0]
        s1 = dat4[1] - dat3[1]
        s2 = dat2[1] - dat1[1]
        s3 = dat2[0] - dat1[0]

        #den = ((dat4[1]-dat3[1])*(dat2[0]-dat1[0]))-((dat4[0]-dat3[0])*(dat2[1]-dat1[1]))
        #den = ((s[1])*(s[3]))-((s[0])*(s[2]))
        den = ((s1)*(s3))-((s0)*(s2))
        if den == 0:
            return False #None
        else:
            s4 = dat1[1] - dat3[1]
            s5 = dat1[0] - dat3[0]
            #ua = (((dat4[0] - dat3[0])*(dat1[1] - dat3[1])) - ((dat4[1] - dat3[1])*(dat1[0] - dat3[0])))/den
            #ub = (((dat2[0] - dat1[0])*(dat1[1] - dat3[1])) - ((dat2[1] - dat1[1])*(dat1[0] - dat3[0])))/den
            #ua = (((s[0])*(s[4])) - ((s[1])*(s[5])))/den
            #ub = (((s[3])*(s[4])) - ((s[2])*(s[5])))/den
            ua = (((s0)*(s4)) - ((s1)*(s5)))/den
            ub = (((s3)*(s4)) - ((s2)*(s5)))/den

            if (ua<0) or (ua>1) or (ub<0) or (ub>1):
                return False #no colision
            else:
                return True #si colision

    for i in p: # la idea es representar cada plataforma como 2 lineas cruzadas diagonales en vez de chequear cada segmento por separado

        iix = i.data['x']
        iiy = i.data['y']
        ww = i.data['w']/2
        hh = i.data['h']/2
        iiyphh = iiy - hh
        iiymhh = iiy + hh
        iixpww = iix - ww
        iixmww = iix + ww
        #if  point_distanceB((i.data['x'],i.data['y']),a1)<dd:

        b1 = (iixmww, iiymhh) #linea superior
        b2 = (iixpww, iiymhh)

        c1 = (iixmww, iiyphh)#linea inferior
        c2 = (iixpww, iiyphh)

        #if not scanC(a1,a2,b1,b2) and not scanC(a1,a2,c1,c2) and not scanC(a1,a2,b1,c1) and not scanC(a1,a2,b2,c2):
        if scanC(a1,a2,b1,b2) or scanC(a1,a2,c1,c2) or scanC(a1,a2,b1,c1) or scanC(a1,a2,b2,c2):
            return i
        else:
            r = None
    return r

def scanOtroMas(a1,a2,dd,p): #tiene que tomar, distancia , punto origen, punto final, obstaculos. tiene que devolver el punto de contacto
    #return True
    ddd=0
    r = [None]
    result = [False,False,False,False,0,0]
    min_dis = [a2[0],a2[1],-1,-1] #x,y,cuanto
    for i in p: # la idea es representar cada plataforma como 2 lineas cruzadas diagonales en vez de chequear cada segmento por separado
        dde = 0
        min_dis[3] = -1
        iix = i.data['x']
        iiy = i.data['y']
        ww = i.data['w']/2
        hh = i.data['h']/2
        iiyphh = iiy - hh
        iiymhh = iiy + hh
        iixpww = iix - ww
        iixmww = iix + ww
        #if  point_distanceB((i.data['x'],i.data['y']),a1)<dd:
        b1 = (iixmww, iiymhh) #linea superior
        b2 = (iixpww, iiymhh)

        c1 = (iixmww, iiyphh)#linea inferior
        c2 = (iixpww, iiyphh)

        for j in range(4):

            dat1 = a1; dat2 = a2;
            if j == 0:
                dat3 = b1; dat4 = b2
            elif j == 1:
                dat3 = c1; dat4 = c2
            elif j == 2:
                dat3 = b1; dat4 = c1
            else:
                dat3 = b2; dat4 = c2

            s0 = dat4[0] - dat3[0]
            s1 = dat4[1] - dat3[1]
            s2 = dat2[1] - dat1[1]
            s3 = dat2[0] - dat1[0]
            den = ((s1)*(s3))-((s0)*(s2))

            if den == 0:
                result[j] = False #None
            else:
                s4 = dat1[1] - dat3[1]
                s5 = dat1[0] - dat3[0]
                ua = (((s0)*(s4)) - ((s1)*(s5)))/den
                ub = (((s3)*(s4)) - ((s2)*(s5)))/den

                if (ua<0) or (ua>1) or (ub<0) or (ub>1):
                    result[j] = False #no colision
                else:
                    result[j] = True
                    aaa = dat1[0] + ua*(dat2[0] - dat1[0])#x del punto de contacto
                    bbb = dat1[1] + ua*(dat2[1] - dat1[1])#y del punto de contacto
                    dde = fast_point_distance(a2,(aaa,bbb))
                    if min_dis[3]<0: min_dis[3]=dde
                    if dde <= min_dis[3]:
                        result[4] = aaa
                        result[5] = bbb
                        min_dis[3] = dde
                    #break #si colision

        if result[0] or result[1] or result[2] or result[3]:
            ddd = fast_point_distance(a2,(result[4],result[5]))#a1 SIEMPRE deberia ser el punto de origen
            if min_dis[2]<0: min_dis[2]=ddd #empieza en -1 asi que tengo que darle un valor inicial
            if ddd <= min_dis[2]:
                min_dis[0] = result[4]
                min_dis[1] = result[5]
                min_dis[2] = ddd##
            #r = [i,result[4],result[5]]
            r = [i,min_dis[0],min_dis[1]]
            #pygame.draw.line(screen,(150,255,100,50),a2,(r[1],r[2]),1)
        #else:
            #r = [None]
    return r
