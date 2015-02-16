# -*- coding: utf-8 -*-

# TO DO:
#
#http://paulbourke.net/geometry/insidepoly/
#http://forums.tigsource.com/index.php?topic=8803.0
#
# Ojos blancos debe correr hacia la luz si no esta persiguiendo al jugador
# mÃƒÆ’Ã‚Âºltiples mapas
#
# Ideas locas:
#-sonido de latido del corazon mas fuerte y frecuente cuando la stamina va llegando a 0
#-checkear colisiones en las esquinas inferiores; si solo hay en una hacer una animacion del personaje trastabillando
#-dividir al personaje en 2: torso y piernas, para permitir animaciones independientes
#-angler fish monster, que de la impresion de que es una puerta o algun item necesario cuando en realidad es un monstruo
#-ruido de viento cuando el jugador esta en un lugar abierto, un sonido mas de tubo cuando esta en un lugar cerrado
#
# -Daniel 'Dancorg' Bassi
# @_Dancorg_
#
# gracias a mattgaviota por arreglar los path y el port temprano a python 2.7

#import cProfile
import os.path

import math
import random
import pickle

import pygame
import pygame.key
import pygame.mouse
import pygame.surface
import pygame.pixelarray
import pygame.color
import pygame.image
import pygame.transform
import pygame.mixer
from pygame.locals import*

from utils import*
from dust import*
from coso import*
from obs import*
from enem import*
from alt_target import*
from quadtree import*
from spark import*

pygame.init()

scan_pr = [0,0]

rnd = random.Random()

size = [800,480] #tamano de la ventana
screen = pygame.display.set_mode(size,pygame.SRCALPHA) #crea una ventana de tamano size
screen_rect = screen.get_rect()
s = pygame.Surface(size,pygame.SRCALPHA)
s.set_colorkey(white)
px = pygame.PixelArray(s)
screen.fill(black)

luz = pygame.Surface.convert_alpha(pygame.image.load("assets/light.png"))

snd_step1 = pygame.mixer.Sound("assets/step1.wav")
snd_step2 = pygame.mixer.Sound("assets/step2.wav")

pygame.display.set_caption("InTheDarkness") #nombre de la ventana

done = False

clock = pygame.time.Clock()
#RESOURCES:

#e_img = pygame.Surface.convert_alpha(pygame.image.load("M.bmp"))

def images( filename, cw, ch): #imagenes = "sprites.png" por ejemplo
	images = []
	all_sprites = pygame.Surface.convert(pygame.image.load(filename))
	all_sprites.set_colorkey((255,255,255,255))
	screen.blit(all_sprites,(0,0))
	w , h = all_sprites.get_size()
	for i in range(int(h/ch)):
		a = []
		for j in range(int(w/cw)):
			a.append(all_sprites.subsurface(j*cw,i*ch,cw,ch))
		images.append(a)
	return images



#diccionario para el mapeo de teclas
Keys = {'up':[K_UP],'down':[K_DOWN],'left':[K_LEFT,],'right':[K_RIGHT],'action1':[K_SPACE], 'action2':[K_LCTRL, K_RCTRL], 'action3':[K_LSHIFT, K_RSHIFT]}

p = coso(s, 20, 0, 9, 15, blue,images("assets/tipito.png",13,15),size, snd_step1) #JUGADOR

platforms = []
lights = []
lights_static = []
lights_static.append(dust(s, 716,367,white,0,100,0,0,0, None,True))


obs_map = [[(False,None) for y in range(int(size[1]/10))] for x in range(int(size[0]/10))] #MATRIZ QUE DIVIDE EL MAPA EN TILES DE 10X10 E INDICA SI ESTAN OCUPADOS POR UN OBSTACULO O NO
#pxl =[]

quad = quadtree(0,0,size[0],size[1],0)

print(os.getcwd())


while True: ################### FOR WINDOWS
	try:
		folder = input("Map name: ").strip("\r") #strip saca las \r de los extremos del string
		mapa = str( os.path.abspath( folder ))
		print(mapa )
		aa=os.path.normcase( "/map.dat")
		bb=os.path.normcase( "/map2.dat")
		mapa1 = mapa + aa
		mapa2 = mapa + bb
		print(mapa1)
		file = open(mapa1,'rb')#.readline()
		map_data = pickle.load(file)
		file2 = open(mapa2,'rb')
		map_data2 = pickle.load(file2)
		print("Map loaded succesfully, I guess :P")
		break
	except:
		print('Map not found, please try again you silly!')

for i in map_data:
	c = brown if i.data['mat'] == 1 else gray
	a = obs(int(i.data['x'] + i.data['w']/2), int(i.data['y'] + i.data['h']/2), i.data['w'], i.data['h'], c,i.data['mat'])
	for ii in range(int(i.data['w']/10)):
		for jj in range(int(i.data['h']/10)):
			obs_map[ii+int(i.data['x']/10)][jj+int(i.data['y']/10)] = (True,a)
	platforms.append(a)
	quad.add_obs(a)

##a = obs(200, 120, 50, 20, brown)#FOR DEBUG ONLY
platforms.append(a)
quad.add_obs(a)

en = []#ENEMIGOS

for i in map_data2:
	x = i.data['x']
	w = i.data['w']/2
	y = i.data['y']
	h = i.data['h']/2
	if i.data['color'] == 'red':
		en.append(enem(int(x+w), int(y+h),15,15, red, 4, 1,images("assets/m1515.png",w,h),size, snd_step2, obs_map))
	if i.data['color'] == 'black':
		en.append(enem(int(x+w), int(y+h),15,15, black, 3, 0,images("assets/m1515.png",w,h),size, snd_step2, obs_map))
	if i.data['color'] == 'gray':
		en.append(enem(int(x+w), int(y+h),21,21, gray, 3, 1,images("assets/m2121.png",w,h),size, snd_step2, obs_map))

ang = cant = 0
start = True
energy = 0
stamina = 50

while done == False:
	screen.fill(black)
	clock.tick(20)
	stop = True
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
				done = True
		if event.type == KEYDOWN:
			if event.key in Keys['up'] and stamina > 3*max_speed:#jump
				if p.can_climb:
					ang = 90
					cant = 10
					p.move(math.radians(ang), math.fabs(cant), platforms+en)
				else:
					stamina -= 3*max_speed
					p.jump(max_speed + 5, platforms+en)
				if event.key in Keys['action1']:
					p.throw_dust(lights, ang, cant, 100)

		if event.type == KEYUP:
			if event.key in Keys['action1']:
				if energy >= 15:
					if pygame.key.get_pressed()[Keys['action2'][0]]:
						p.throw_dust(lights, ang, cant, energy,p)
					else:
						p.throw_dust(lights, ang, cant, energy)
				energy = 0

	if pygame.key.get_pressed()[Keys['down'][0]]:#crouch
		ang = 90
		if cant > 0: ang = 0
		if cant > -max_speed: cant -= 1
		#en.jump(11,platforms+[p])
	if pygame.key.get_pressed()[Keys['left'][0]]:
		stop = False
		ang = 180
		if cant > 0: ang = 0
		if cant > -max_speed: cant -= 1
		else: cant = -max_speed
	if pygame.key.get_pressed()[Keys['right'][0]]:
		stop=False
		ang = 0
		if cant < 0: ang = 180
		if cant < max_speed: cant += 1
		else: cant = max_speed
	if pygame.key.get_pressed()[Keys['action1'][0]]:
		if energy < 100:
			energy += 5
	if stop: #para que frene progresivamente
		if cant > 0:
			cant -= 1
		if cant < 0:
			cant += 1
	if pygame.key.get_pressed()[Keys['action3'][0]] and stamina >0:
		max_speed = 3
	else:
		max_speed = 1
	if pygame.mouse.get_pressed()[0] == True:
		print(pygame.mouse.get_pos())

	if math.fabs(cant) > 1 and p.can_jump:
		stamina -= 0.5
	elif stamina < 50 and p.can_jump:
		stamina += 1
	if stamina <= 0:
		max_speed = 1

	px = pygame.PixelArray(s) #el pixel array para hacer la fog of war
   #pygame.draw.line( screen ,green ,p.get_pos() ,pygame.mouse.get_pos() ,5)
	p.move(math.radians(ang), math.fabs(cant), platforms+en)
	p.gravity(platforms + en)

	#pygame.draw.rect(screen, p.data['color'], p.get_pos_size(), 0)#dibuja al jugador
	#pygame.draw.rect(screen, p.cur_anim, p.get_pos_size(), 0)#dibuja al jugador con animaciones
	if ang == 180:
		p.cur_animB = pygame.transform.flip(p.cur_anim,True,False)
		screen.blit(p.cur_animB,(p.data['x']-2-p.data['w']/2,p.data['y']-p.data['h']/2))
	else:
		screen.blit(p.cur_anim,(p.data['x']-2-p.data['w']/2,p.data['y']-p.data['h']/2))

	for i in en:
		enB = en[:]#clonar la lista con slice, para evitar el aliasing molesto
		for j in range(len(enB)):
			if enB[j] == i:
				del enB[j]# se elimina a si mismo de la lista de enemigos
				break
		i.gravity(platforms + [p] + enB)
		i.behave_simple(p,platforms + enB)#IA basica
		if i.data['type'] == 1:
			if i.dir == 180:
				i.cur_animB = pygame.transform.flip(i.cur_anim,True,False)
				screen.blit(i.cur_animB,(i.data['x']-2-i.data['w']/2,i.data['y']-i.data['h']/2))
			else:
				screen.blit(i.cur_anim,(i.data['x']-2-i.data['w']/2,i.data['y']-i.data['h']/2))
#            screen.blit(i.cur_anim,(i.data['x']-2-i.data['w']/2,i.data['y']-i.data['h']/2))
		#pygame.draw.rect(screen,i.data['color'],i.get_pos_size(),0)#dibuja al enemigo
		i.illum = False#es importante que este al final de todas las funciones para que no resetee el valor antes de tiempo
	p.illum = False #es importante que este al final de todas las funciones para que no resetee el valor antes de tiempo


	for i in platforms:#dibuja las plataformas
		pygame.draw.rect(screen,i.get_color(),i.get_pos_size(),0)

##    if start: #esto era para hacer pruebas de optimizacion, para darle update a toda la pantalla 1 vez y luego solo a los objetos que se mueven
##        start=False
##        pygame.display.update()

	s.fill(black) #pinta todo de negro por encima de los objetos del juego
	#pygame.draw.circle(s,(0,0,0,100),(600,100),200,0)

	for i in range(int(p.data['x'] - 15), int(p.data['x'] + 15)):#borra un rectangulo de la superficie negra..
		for j in range(int(p.data['y'] - 15), int(p.data['y'] + 15)):
			if i > 0 and i < size[0] and j > 0 and j < size[1]:#si sale de la pantalla crashea
				if((i-p.data['x'])**2 + (j-p.data['y'])**2) <= 225:
					px[int(i)][int(j)] = (0,0,0,150)#..y lo pinta de este color

	for i in lights:
############################# PRETTY MUCH FASTER BUT VERY UGLY
		#pygame.draw.circle(s,(255,255,100,30),(int(i.data['x']),int(i.data['y'])),i.data['intensity'],0)
		dat = i.data
		qual = 6 #calidad del circulo
		qual2 = qual*qual
		inte = int(dat['intensity']/qual)#radio sobre calidad
		mm = dat['intensity']**2
		ll = []

		#ll += quad.retrieve(i) + en +[p]


		for ddd in platforms+en: #ESTA PARTE DEBE SER REEMPLAZADA POR LA INTERACCION CON EL QUADTREE
			if fast_point_distance(ddd.get_pos(),(dat['x'],dat['y'])) < mm + ddd.data['w']+ddd.data['h']:
				#if not scan(ddd, i, platforms+en+[p]):
					#ll[ddd]=(ddd)
					ll.append(ddd)

		lll = ll #+ [p]

		if fast_point_distance(p.get_pos(),(dat['x'],dat['y'])) > 60:
			lll = lll + [p]

		#print(len(ll))

		radio = inte/math.sqrt(2)

		i.plotCircle(dat['x'],dat['y'],radio,qual,lll)
		luz2 = pygame.transform.scale(luz,(dat['intensity'],dat['intensity']))
		screen.blit(luz2,(dat['x']-luz2.get_width()/2,dat['y']-luz2.get_height()/2),)

		for e in en + [p]:
			b = scanOtro((dat['x'],dat['y']),(e.data['x'],e.data['y']),dat['intensity']+qual,lll)#platforms+en+[p])
			if (b == None or b == e) and fast_point_distance((dat['x'],dat['y']),(e.data['x'],e.data['y']))< mm:
				e.illum = True
		#print(p.illum)
#        for j in range(-inte,inte): #recorre el area iluminada(cuadrado)
#            jjq = j*j*qual2
#            for k in range(-inte,inte):
#                if (jjq + k*k*qual2) <= (dat['intensity'] - qual)**2:# solo los pixeles que estan dentro del circulo
#                    xx = int(j*qual+dat['x'])
#                    yy = int(k*qual+dat['y'])
#                    dd = int(fast_point_distance((dat['x'],dat['y']),(xx,yy)))
#                    #b = scanOtro((dat['x'],dat['y']),(xx,yy),dat['intensity']+qual,lll)#platforms+en+[p])
#                    b = scanOtroMas((dat['x'],dat['y']),(xx,yy),dat['intensity']+qual,lll)[0]#platforms+en+[p])
#                    if b == None:
#                        pygame.draw.circle(s,(255,255,100,int(40*(mm-dd)/mm)),(xx,yy),qual,0)
#                        #pygame.draw.circle(s,(255,255,100,30),(xx,yy),qual,0)
#                    elif b.__class__.__name__ == 'coso' or b.__class__.__name__ == 'enem':
#                        b.illum = True
#                        #pygame.draw.circle(s,(255,255,100,int(10*(mm-dd)/mm)),(xx,yy),qual,0)5

		i.chispita.append(spark(dat['x'], dat['y'], size))
		for chisp in i.chispita:
			 chisp.update(px,i.chispita)

############################################################## SOMBRAS POR POLIGONOS ###########################################
##        for j in ll:
##
##            esquinas = []
##            a = (j.data['x']-j.data['w']/2,j.data['y']-j.data['h']/2)
##            if scan((i.data['x'],i.data['y']),a,ll,False) != None: #Not sure if chequea la colision consigo mismo
##                esquinas.append(a)
##                pygame.draw.line(s,black,a,(i.data['x'],i.data['y']),1)
##
##            a = (j.data['x']-j.data['w']/2,j.data['y']+j.data['h']/2)
##            if scan((i.data['x'],i.data['y']),a,ll,False) == None: #Not sure if chequea la colision consigo mismo
##                esquinas.append(a)
##                pygame.draw.line(s,white,a,(i.data['x'],i.data['y']),1)
##
##            a = (j.data['x']+j.data['w']/2,j.data['y']-j.data['h']/2)
##            if scan((i.data['x'],i.data['y']),a,ll,False) == None: #Not sure if chequea la colision consigo mismo
##                esquinas.append(a)
##                pygame.draw.line(s,green,a,(i.data['x'],i.data['y']),1)
##
##            a = (j.data['x']+j.data['w']/2,j.data['y']+j.data['h']/2)
##            if scan((i.data['x'],i.data['y']),a,ll,False) == None: #Not sure if chequea la colision consigo mismo
##                esquinas.append(a)
##                pygame.draw.line(s,blue,a,(i.data['x'],i.data['y']),1)
##            #esquinas.append((i.data['x'],i.data['y']))
##            print (esquinas)



##            if len(esquinas)>2:
##                pygame.draw.polygon(s,black,esquinas,0)

			#j.polygon(i,i.data['intensity'])

			# 0. dibujar el circulo de luz DONE
			# 1. identificar los 2/3 puntos mas cercanos a la luz
			# 1b. identificar los 2 mas separados si son 3
			# 1.BIS usar scan para ver cuales puntos son visibles desde la luz
			# 2. crear 3 puntos
			# 2.1 usando los 2 puntos extremo extender una linea hasta el borde la luz(o mas alla, pensar en el caso de que la superficie cubra 180 grados de l luz)
			# 2.2 crear el 3 punto entre los otros 2 para evitar la secante entre ellos
			# 3. dibujar el poligono
			# 4. usar scan con los enemigos y jugador para setear el illum

##            def polygon(self,origin,intensity):
##                normal=((origin.data['x'],origin.data['y']),(self.data['x'],self.data['y']))

###############################################################################################

		lsize = rnd.randrange(2,5,1)
		pygame.draw.circle(s,(255,240,190,50*lsize),(int(dat['x']),int(dat['y'])),lsize,0)
		i.update(platforms,lights)

###############################################################################

	mmm = pygame.mouse.get_pos()
	if obs_map[int(mmm[0]/10)][int(mmm[1]/10)][0] == True:
		pygame.draw.circle(screen,(0,255,0),(mmm[0],mmm[1]),6,0)

	for i in lights_static:
		dat = i.data
		#dat['x'] = mmm[0]
		#dat['y'] = mmm[1]
		qual = 8 #calidad del circulo
		qual2 = qual*qual
		inte = int(dat['intensity']/qual)#radio sobre calidad
		mm = dat['intensity']**2
		if len(i.ll) == 0:
			for ddd in platforms: #ESTA PARTE DEBE SER REEMPLAZADA POR LA INTERACCION CON EL QUADTREE
				if fast_point_distance(ddd.get_pos(),(dat['x'],dat['y'])) < mm + ddd.data['w']+ddd.data['h']:
					i.ll.append(ddd)

		lll = i.ll + en

		if fast_point_distance(p.get_pos(),(dat['x'],dat['y'])) > 60:
			lll = lll + [p]

		radio = inte/math.sqrt(2)

		i.plotCircle(dat['x'],dat['y'],radio,qual,lll)
		luz2 = pygame.transform.scale(luz,(dat['intensity'],dat['intensity']))
		screen.blit(luz2,(dat['x']-luz2.get_width()/2,dat['y']-luz2.get_height()/2),)

		for e in en + [p]:
			b = scanOtro((dat['x'],dat['y']),(e.data['x'],e.data['y']),dat['intensity']+qual,lll)#platforms+en+[p])
			if (b == None or b == e) and fast_point_distance((dat['x'],dat['y']),(e.data['x'],e.data['y']))< mm:
				e.illum = True

		lsize = rnd.randrange(2,5,1)
		pygame.draw.circle(s,(255,240,190,50*lsize),(int(dat['x']),int(dat['y'])),lsize,0)
###############################################################################

	for i in en:
		i.ojitos(lights+lights_static,platforms,p,px)

	if energy > 0:
		pygame.draw.line(s,yellow2,(50,5),(energy*3+50,5),5) # barra de energia de la bengala
	if stamina > 0:
		 pygame.draw.line(s,blue,(50,10),(stamina*3+50,10),5)
	del(px)

	screen.blit(s, (0,0))

	pygame.display.update()
