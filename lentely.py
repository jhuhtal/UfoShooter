import pygame
import math
import random
import time

screen_w=1200
screen_h=900

s=input('Fullscreen or Window?\n')

if s in ('f','F','fullscreen','Fullscreen'):
    pygame.init()
    Display=pygame.display.set_mode((screen_w,screen_h),pygame.FULLSCREEN)

if s in ('w','W','window','Window'):
    pygame.init()
    Display=pygame.display.set_mode((screen_w,screen_h))

pygame.display.set_caption('Ufo Shooter -- press r to restart')

global clock
clock = pygame.time.Clock()

pygame.mouse.set_visible(False)

black=(0,0,0)
white=(255,255,255)
green=(0,100,0)
bright_blue=(30,144,255)
yellow=(255,242,0)
comm_blue=(120,120,255)
comm_red=(255,40,40)

interface_image=pygame.image.load('interface1.png')
interface_image.set_colorkey(white)
interface_x_left=20
interface_x_right=1020
interface_y_up=20
interface_y_down=880

halli=pygame.image.load('halli.png')
halli.set_colorkey(white)
halli_w=133
halli_h=37

alusta=pygame.image.load('alusta.png')
alusta.set_colorkey(white)
alusta_h=31
alusta_w=30

paja=pygame.image.load('paja.png')
paja.set_colorkey(white)
paja_h=17
paja_w=20

kerrostalo=pygame.image.load('kerrostalo.png')
kerrostalo_h=83
kerrostalo_w=32

kerrostalo2=pygame.image.load('kerrostalo2.png')
kerrostalo2_h=63
kerrostalo2_w=32

kerrostalo3=pygame.image.load('kerrostalo3.png')
kerrostalo3_h=43
kerrostalo3_w=32

komentokeskus=pygame.image.load('komentokeskus.png')
komentokeskus_w=62
komentokeskus_h=43
komentokeskus.set_colorkey(white)

projectile_img=pygame.image.load('projectile_white.png')
projectile_img.set_colorkey(white)

exp_yellow=pygame.image.load('exp_yellow.png')
exp_yellow.set_colorkey(white)
exp_red=pygame.image.load('exp_red.png')
exp_red.set_colorkey(white)

debris_grey=pygame.image.load('debris_grey.png')
debris_grey.set_colorkey(white)
debris_light_grey=pygame.image.load('debris_light_grey.png')
debris_light_grey.set_colorkey(white)

ufo1=pygame.image.load('ufo1.png')
ufo1.set_colorkey(white)
ufo2=pygame.image.load('ufo2.png')
ufo2.set_colorkey(white)

ship1_line=pygame.image.load('ship1_line.png')
ship1_line_red=pygame.image.load('ship1_line_red.png')

ground_height=100
global explosion_detail
explosion_detail=150
global gravity
gravity=0.013
global projectiles
projectiles=[]
global debris
debris=[]
global explosion_particles
explosion_particles=[]
global buildings
buildings=[]
global ufot
ufot=[]

font_terminal=pygame.font.Font('terminal2.ttf',10)
font_terminal_large=pygame.font.Font('terminal2.ttf',11)
global message_list
message_list=[]
global console_lines
console_lines=[]

global speed
speed=0
global speed_timer
speed_timer=time.clock()
global target_dist
target_dist=font_terminal.render('Target: N/A',1,yellow)
global target_time
target_time=time.clock()

target_x=0
target_y=0

class Building:
    def __init__(self,building_type,x,y):
        self.hp=200
        self.building_type=building_type
        if building_type==halli:
            self.image=halli
            self.w=133
            self.h=37
            self.x=x
            self.y=y
        elif building_type==alusta:
            self.image=alusta
            self.h=31
            self.w=30
            self.x=x
            self.y=y
        elif building_type==paja:
            self.image=paja
            paja.set_colorkey(white)
            self.h=17
            self.w=20
            self.x=x
            self.y=y
        elif building_type==kerrostalo:
            self.image=kerrostalo
            self.h=83
            self.w=32
            self.x=x
            self.y=y

        elif building_type==kerrostalo2:
            self.image=kerrostalo2
            self.h=63
            self.w=32
            self.x=x
            self.y=y
        elif building_type==kerrostalo3:
            self.image=kerrostalo3
            self.h=43
            self.w=32
            self.x=x
            self.y=y
        elif building_type==komentokeskus:
            self.image=komentokeskus
            komentokeskus.set_colorkey(white)
            self.w=62
            self.h=43
            self.x=x
            self.y=y
        self.mask=pygame.mask.from_surface(self.image)
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)


def draw_buildings():
    for i in range(0,len(buildings)):
        if buildings[i]!=0 and buildings[i].building_type!=alusta:
            Display.blit(buildings[i].image,(buildings[i].rect))
            #print(buildings[i].building_type,buildings[i].rect)

def draw_alusta():
    for i in range(0,len(buildings)):
        if buildings[i]!=0 and buildings[i].building_type==alusta:
            Display.blit(buildings[i].image,(buildings[i].rect))

class Projectile:
    def __init__(self,x,y,dx,dy):
        self.x=x
        self.y=y
        self.dx=dx
        self.dy=dy
        self.mass=0
        self.mass_timer=time.clock()
        self.mask=pygame.mask.from_surface(projectile_img)
        self.rect=projectile_img.get_rect()
        self.rect.center=(x,y)
        

def projectile_manager():
    empty_elements=0
    global projectiles
    for i in range(0,len(projectiles)):
        if projectiles[i]!=0:
            if 0>projectiles[i].x or projectiles[i].x>screen_w or projectiles[i].y<0 or projectiles[i].y>screen_h-105:
                projectiles[i]=0
            else:
                projectiles[i].x+=projectiles[i].dx
                projectiles[i].y+=projectiles[i].dy
                projectiles[i].dy+=gravity
                #projectiles[i].rect=pygame.Rect(projectiles[i].x,projectiles[i].y,3,3)
                projectiles[i].rect.center=(projectiles[i].x,projectiles[i].y)
                #projectiles[i].mask=pygame.mask.from_surface(projectile_img)
                projectiles[i].mask.fill()
                Display.blit(projectile_img,(projectiles[i].rect))
                if projectiles[i].mass==0 and time.clock()-projectiles[i].mass_timer>0.1:
                    projectiles[i].mass=1
        else:
            empty_elements+=1
            if empty_elements==len(projectiles):
                projectiles=[]

class Debris:
    def __init__(self,x,y,dx,dy,color):
        self.x=x
        self.y=y
        self.dx=dx
        self.dy=dy
        self.mass=5
        self.color=color
        self.mask=pygame.mask.from_surface(debris_grey)
        if self.color=='grey':
            self.img=debris_grey
        elif self.color=='light_grey':
            self.img=debris_light_grey
        self.rect=self.img.get_rect()

def debris_manager():
    empty_elements=0
    global debris
    for i in range(0,len(debris)):
        if debris[i]!=0:
            if 0>debris[i].x or debris[i].x>screen_w or debris[i].y<0 or debris[i].y>screen_h-105:
                debris[i]=0
            else:
                debris[i].x+=debris[i].dx
                debris[i].y+=debris[i].dy
                debris[i].dy+=1.5*gravity
                debris[i].rect=debris[i].img.get_rect()
                debris[i].rect.center=(debris[i].x,debris[i].y)
                debris[i].mask=pygame.mask.from_surface(debris[i].img)
                debris[i].mask.fill()
                Display.blit(debris[i].img,(debris[i].rect))
        else:
            empty_elements+=1
            if empty_elements==len(debris):
                debris=[]
                
def create_debris(x,y,dx,dy,color,debris_q):
    global debris
    for i in range(0,debris_q):
        debris_x=x+random.randint(-8,8)
        debris_y=y+random.randint(-8,8)
        debris_dx=dx+random.uniform(-2,2)
        debris_dy=dy+random.uniform(-2,2)
        debris.append(Debris(debris_x,debris_y,debris_dx,debris_dy,color))

class Explosion_particle:
    def __init__(self,x,y,dx,dy,color,damage):
        self.timer=time.clock()
        self.x=x
        self.y=y
        self.dx=dx
        self.dy=dy
        self.color=color
        self.damage=damage
        if self.color=='red':
            self.img=exp_red
        if self.color=='yellow':
            self.img=exp_yellow
        if self.damage==1:
            self.life=random.uniform(1,4)
        else:
            self.life=random.uniform(0.2,0.7)         

def create_explosion(x,y,dx,dy,q,damage):
    global explosion_particles
    for i in range(0,q):
        angle=random.uniform(0,2*math.pi)
        exp_x=x+(-8*math.cos(angle))
        exp_y=y+(8*math.sin(angle))
        exp_dx=random.uniform(-2*math.cos(angle),2*math.cos(angle))+0.6*dx
        exp_dy=random.uniform(-2*math.sin(angle),2*math.sin(angle))+0.6*dy
        if random.randint(1,3)==1:
            color='red'
        else:
            color='yellow'
        explosion_particles.append(Explosion_particle(exp_x,exp_y,exp_dx,exp_dy,color,damage))

def explosion_manager():
    empty_elements=0
    global explosion_particles
    for i in range(0,len(explosion_particles)):
        if explosion_particles[i]!=0:
            if 0>explosion_particles[i].x or explosion_particles[i].x>screen_w or explosion_particles[i].y<0 or explosion_particles[i].y>screen_h-ground_height:
                explosion_particles[i]=0
            else:
                explosion_particles[i].x+=explosion_particles[i].dx
                explosion_particles[i].y+=explosion_particles[i].dy
                explosion_particles[i].y+=-0.6*gravity
                explosion_particles[i].rect=explosion_particles[i].img.get_rect()
                explosion_particles[i].rect.center=(explosion_particles[i].x,explosion_particles[i].y)
                explosion_particles[i].mask=pygame.mask.from_surface(explosion_particles[i].img)
                explosion_particles[i].mask.fill()
                Display.blit(explosion_particles[i].img,(explosion_particles[i].rect))
                if time.clock()-explosion_particles[i].timer>=explosion_particles[i].life:
                    explosion_particles[i]=0
                    
        else:
            empty_elements+=1
            if empty_elements==len(explosion_particles):
                explosion_particles=[]                 
               
class Ship:

    def __init__(self,x,y,dx,dy,ddx,ddy,angle,dangle):
        self.x=x
        self.y=y
        self.dx=dx
        self.dy=dy
        self.ddx=ddx
        self.ddy=ddy
        self.angle=angle
        self.dangle=dangle
        self.rect=pygame.image.load('ship1_grey.png').get_rect()
        self.rect.center=(x,y)
        self.mask=pygame.mask.from_surface(pygame.image.load('ship1_grey.png'))
        self.h=31
        self.hp=100
        self.temp=10
        self.mass=100
        self.vector=pygame.math.Vector2(math.cos(math.radians(angle)),math.sin(math.radians(angle)))
        self.unit_vector=pygame.math.Vector2.normalize(self.vector)
        self.max_speed=4.6
        self.thruster_on=False
        self.thruster_right_on=False
        self.thruster_left_on=False
        self.shoots=False
        self.alive=True
        self.hit_timer=time.clock()

    def position(self,x,y,dx,dy,ddx,ddy,dangle):     
        global gravity
        global explosion_detail
        self.dx+=ddx
        self.dy+=ddy+gravity
        if self.dy>=self.max_speed:
            self.dy=self.max_speed
        if self.dy<=-self.max_speed:
            self.dy=-self.max_speed
        if self.dx>=self.max_speed:
            self.dx=self.max_speed
        if self.dx<=-self.max_speed:
            self.dx=-self.max_speed
        self.x+=dx
        self.y+=dy
        self.angle+=dangle
        if self.y>=screen_h-ground_height-12 and self.dy>0:
            #print(math.sqrt(ship.dx**2+ship.dy**2))
            ship.dy=-0.1*dy
            ship.dx=0
            if math.sqrt(ship.dx**2+ship.dy**2)>0.13:
                damage=(3*math.sqrt(ship.dx**2+ship.dy**2))**2*ship.mass
                self.hp+=-damage
                self.hit_timer=time.clock()
        self.temp+=-0.02
        if self.temp<10:
            self.temp=10
        if self.temp>100:
            create_debris(self.x,self.y,self.dx,self.dy,'grey',6)
            create_explosion(ship.x,ship.y,ship.dx,ship.dy,explosion_detail,1)
            self.alive=False
        if ship.hp<=0:
            create_debris(self.x,self.y,self.dx,self.dy,'grey',6)
            create_explosion(ship.x,ship.y,ship.dx,ship.dy,explosion_detail,1)
            self.alive=False
        if self.alive==False:
            print_message('>Ship destroyed. Mission failed.',(255,40,40))

            
        #print(self.x,self.y)
        
               
    def thrust(self):
        self.thrust_power=0.009*math.sqrt(self.dx**2+self.dy**2)+0.03
        self.vector=pygame.math.Vector2(math.cos(math.radians(self.angle)),math.sin(math.radians(self.angle)))
        self.unit_vector=pygame.math.Vector2.normalize(self.vector)
        thrust_vector=self.unit_vector*self.thrust_power
        self.ddx=thrust_vector[0]
        self.ddy=-thrust_vector[1]
        self.temp+=0.026
        
    def shoot(self):
        self.vector=pygame.math.Vector2(math.cos(math.radians(self.angle)),math.sin(math.radians(self.angle)))
        self.unit_vector=pygame.math.Vector2.normalize(self.vector)
        projectile_speed_vector=10*self.unit_vector
        dx=projectile_speed_vector[0]+self.dx
        dy=-projectile_speed_vector[1]+self.dy
        self.dx+=-1/self.mass*dx
        self.dy+=-1/self.mass*dy
        x=self.rect.center[0]
        y=self.rect.center[1]
        projectiles.append(Projectile(x,y,dx,dy))
        self.temp+=0.2

    def draw(self,x,y,angle):                    
        surface=pygame.Surface((31,22))
        #if ship.shoots==True:
        #surface.blit(pygame.image.load('ship1_grey_shoots.png'),(0,0))
        if self.thruster_on==False and ship.thruster_right_on==False and ship.thruster_left_on==False:
            surface.blit(pygame.image.load('ship1_grey.png'),(0,0))
        elif self.thruster_on==True:
            if self.thruster_right_on==True:
                surface.blit(pygame.image.load('ship1_grey_back_right_thruster.png'),(0,0))
            elif ship.thruster_left_on==True:
                surface.blit(pygame.image.load('ship1_grey_back_left_thruster.png'),(0,0))
            else:
                surface.blit(pygame.image.load('ship1_grey_back_thruster.png'),(0,0))
        elif self.thruster_right_on==True:
            surface.blit(pygame.image.load('ship1_grey_right_thruster.png'),(0,0))
        elif self.thruster_left_on==True:
            surface.blit(pygame.image.load('ship1_grey_left_thruster.png'),(0,0))
        rect1=surface.get_rect()
        rect1.center=(x,y)
        surface.set_colorkey((255,255,255))
        rotated_surface=pygame.transform.rotate(surface,angle)
        self.rect=rotated_surface.get_rect()
        self.rect.center=rect1.center
        rotated_surface.set_colorkey((255,255,255))
        self.mask=pygame.mask.from_surface(rotated_surface)
        Display.blit(rotated_surface,(self.rect))

def metrics(x,y):
    global speed
    global speed_timer
    global target_dist
    global target_time
    angle=ship.angle
    if time.clock()-speed_timer>0.2:
        speed=int(math.sqrt(ship.dx**2+ship.dy**2)*0.21*60*60*60/1000)
        speed_timer=time.clock()
    speed_meter = font_terminal.render('Velocity: '+str(speed)+' km/h',1,yellow)
    Display.blit(speed_meter, (1045, 394))
    altitude = font_terminal.render('Altitude: '+str(int((900-ship.y-ground_height-12)*0.48))+' m',1,yellow)
    Display.blit(altitude, (1045, 413))
    if time.clock()-target_time>0.5:
        target_dist=font_terminal.render('Target: '+str(int(math.sqrt((ship.rect.midbottom[0]-x)**2+(ship.rect.midbottom[1]-y)**2)*0.48))+' m',1,yellow)
        target_time=time.clock()
    Display.blit(target_dist, (1045, 432))

def print_message(message,color):
    rects_width=0
    width_counter=0
    word_counter=0
    global console_lines
    message_rects=[]
    message_words=[]
    message_split=message.split(' ')
    for i in range(0,len(message_split)):
        message_words.append(font_terminal_large.render(message_split[i]+' ',1,color))
        message_rects.append(message_words[i].get_rect())
        #message_element=[message_words,message_rects]
        #message_list.append(message_element)
        rects_width+=message_rects[i].width
    if rects_width<=143:
        console_lines.append(message_words)
    else:
        for i in range(0,len(message_words)):
            width_counter+=message_rects[i].width
            word_counter+=1
            if width_counter+message_rects[i].width>=143:
                console_lines.append(message_words[i-word_counter+1:i+1])
                width_counter=0
                word_counter=0               
            elif i==len(message_words)-1:
                console_lines.append(message_words[i-word_counter+1:i+1])
                width_counter=0
                word_counter=0               

            if len(console_lines)>=24:
                console_lines=console_lines[len(console_lines)-23:24]
    if len(console_lines)>=24:
        console_lines=console_lines[len(console_lines)-23:24]


def console():
    global console_lines
    width=0
    #screen=pygame.Rect(1035,584,148,282)
    for i in range(0,len(console_lines)):
        for j in range(0,len(console_lines[i])):
            if j==0:
                Display.blit(console_lines[i][j],(1035,584+i*12))
                width=console_lines[i][j].get_width()
                

            else:
                Display.blit(console_lines[i][j],(1035+width,584+i*12))
                width+=console_lines[i][j].get_width()

        width=0
                
def secondary_weapon():
    #secondary_weapon = font_terminal.render('Secondary weapon:',1,yellow)
    na= speed_meter = font_terminal.render('Not available',1,yellow)
    #Display.blit(secondary_weapon, (1045, 486))
    Display.blit(na,(1062, 508)) 

def lifebar():
    pygame.draw.rect(Display,(80,80,80),(1058,210,100,8))
    pygame.draw.rect(Display,(60,60,60),(1058,218,100,10))       
    if ship.alive==True:
        pygame.draw.rect(Display,(200,0,0),(1058,210,ship.hp,8))
        pygame.draw.rect(Display,(180,0,0),(1058,218,ship.hp,10))
    structural_integrity = font_terminal.render('Structural integrity',1,yellow)
    Display.blit(structural_integrity, (1039, 243))

def tempbar():
    pygame.draw.rect(Display,(80,80,80),(1058,308,100,8))
    pygame.draw.rect(Display,(60,60,60),(1058,316,100,10))
    pygame.draw.rect(Display,(180,180,0),(1058,308,ship.temp,8))
    pygame.draw.rect(Display,(160,160,0),(1058,316,ship.temp,10))
    core_temperature = font_terminal.render('Core temperature',1,yellow)
    Display.blit(core_temperature, (1052, 340))

def ship_line(x,y,angle):
    surface1=pygame.Surface((41,23))
    if ship.alive==False or time.clock()-ship.hit_timer<0.8 and time.clock()>0.8:
        surface1.blit(ship1_line_red,(0,0))
    else:
        surface1.blit(ship1_line,(0,0))
    rect1=surface1.get_rect()
    rect1.center=(x,y)
    surface1.set_colorkey((255,255,255))
    rotated_surface=pygame.transform.rotate(surface1,angle)
    ship_line_rect=rotated_surface.get_rect()
    ship_line_rect.center=rect1.center
    rotated_surface.set_colorkey((255,255,255))
    Display.blit(rotated_surface,(ship_line_rect))

global start_message_counter
start_message_counter=0
global start_timer
start_timer=time.clock()
global mission_start
mission_start=False
global r
r=0
global hp_warning
hp_warning=False
global temp_warning
temp_warning=False

def message_manager():
    global mission_start
    global start_message_counter
    global start_timer
    global r
    global hp_warning
    global temp_warning
    if mission_start==True:
        launch_messages=['>Initiating ship control console...','>Checking system status...','>Main generator running','>Measurement and control systems running','>Core temperature stabile',
                         '>Gun controls active','>Igniting thrusters...','>Activating thruster control...','>All systems OK. Ship ready for launch.']
        if start_message_counter==0:
            r=random.uniform(0.2,1.5)
        if time.clock()-start_timer>r and start_message_counter<=len(launch_messages)-1:
            print_message(launch_messages[start_message_counter],yellow)
            start_message_counter+=1
            r=random.uniform(0.2,1.5)
            start_timer=time.clock()
        if start_message_counter>=len(launch_messages)-1 and time.clock()-start_timer>r*2:
            print_message('>"This is it, Captain. We are detecting a small squad of enemy aircraft closing in. Protect the command center at all costs. Good luck!"',(130,130,255))
            mission_start=False
    if ship.hp<20 and hp_warning==False:
        print_message('>WARNING: Ship hull severely damaged',comm_red)
        hp_warning=True
    if ship.temp>80 and temp_warning==False:
        print_message('>WARNING: Reactor core unstable',comm_red)
        temp_warning=True
    
   
def interface():
    Display.blit(interface_image,(0,0))
    ship_line(1104,95,ship.angle)
    lifebar()
    tempbar()
    metrics(target_x,target_y)
    secondary_weapon()
    message_manager()
    console()
    
global ship
ship=Ship(120+alusta_w/2,screen_h-100-31/2+2,0,0,0,0,90,0)      #älä poista

class Ufo:
    def __init__(self,x,y,dx,dy,ufo_type):
        self.x=x
        self.y=y
        self.dy=dy
        self.dx=dx
        self.ddx=0
        self.ddy=0
        self.type=ufo_type
        self.shoot_timer=time.clock()
        self.hp=40
        self.mass=75
        self.colliding=False
        self.can_collide=True
        self.colliding_dx=0
        self.colliding_dy=0
        self.colliding_timer=0
        self.colliding_timer2=0
        self.evasion=True
        self.evasion_timer=0

        if self.type==1:
            self.hp=40
            self.mass=75
            self.rect=ufo1.get_rect()
            self.rect.center=(x,y)
            self.max_speed=3
            self.mask=pygame.mask.from_surface(ufo1)
            self.w=36
            self.h=16

        if self.type==2:
            self.hp=50
            self.mass=100
            self.rect=ufo2.get_rect()
            self.rect.center=(x,y)
            self.max_speed=4
            self.mask=pygame.mask.from_surface(ufo2)
            self.w=36
            self.h=16

           
        self.ingame=False
        
    def draw(self,x,y):
        #surface=pygame.Surface((self.w,self.h))
        #surface.set_colorkey((255,255,255))

        if self.type==1:
            self.rect=ufo1.get_rect()
            self.rect.center=(x,y)
            self.mask=pygame.mask.from_surface(ufo1)
            self.mask.fill()
            Display.blit(ufo1,(self.rect))
        if self.type==2:
            self.rect=ufo2.get_rect()
            self.rect.center=(x,y)
            self.mask=pygame.mask.from_surface(ufo2)
            self.mask.fill()
            Display.blit(ufo2,(self.rect))
       
    def position(self,x,y,dx,dy):

        if time.clock()-self.colliding_timer2>0.25:
            self.can_collide=True
            
        if self.type==1 or self.type==2:
            if self.colliding==True and time.clock()-self.colliding_timer<1:
                self.dx=self.colliding_dx
                self.dy=self.colliding_dy+1.5*gravity
                self.x+=self.colliding_dx
                self.y+=self.colliding_dy

            else:

                self.colliding=False
                
                if self.evasion==False and time.clock()-self.evasion_timer>0.5:
                    self.evasion=True
              
                self.dx+=self.ddx
                self.dy+=self.ddy

                if self.dy>=self.max_speed:
                    self.dy=self.max_speed-0.001
                if self.dy<=-self.max_speed:
                    self.dy=-self.max_speed-0.001
                if self.dx>=self.max_speed:
                    self.dx=self.max_speed-0.001
                if self.dx<=-self.max_speed:
                    self.dx=-self.max_speed-0.001
                       
                self.x+=dx
                self.y+=dy

                self.ddx=random.uniform(-0.2,0.2)
                self.ddy=random.uniform(-0.5,0.5)

                if self.x>=1020-100:
                    self.ddx=-0.2
                elif self.x<=20+100:
                    self.ddx=0.2
                if self.y>=660:
                    self.ddy=-0.2
                elif self.y<=20+160:
                    self.ddy=0.2
                if self.y+self.h>=730:
                    self.dy=-0.1

        if self.y>=screen_h-ground_height-int(self.h/2) and self.dy>0:
            self.dy=-0.1*dy
            self.dx=0
            if math.sqrt(self.dx**2+self.dy**2)>0.13:
                damage=(3*math.sqrt(self.dx**2+self.dy**2))**2*self.mass
                self.hp+=-damage

        if self.hp<=0:
            create_debris(self.x,self.y,self.dx,self.dy,'light_grey',6)
            create_explosion(self.x,self.y,self.dx,self.dy,explosion_detail,1)

    def shoot(self):
        if self.type==1:
            if time.clock()-self.shoot_timer>0.2:
                self.vector=pygame.math.Vector2(ship.x-self.x,-(ship.y-self.y))
                if ship.x>0 and ship.x<1020 and ship.y>0 and ship.alive==True:
                    a=random.randint(1,3)
                    if a<3:
                        self.vector=pygame.math.Vector2(ship.x-self.x,-(ship.y-self.y))
                    else:
                        self.vector=pygame.math.Vector2(buildings[4].rect.center[0]-self.x,-(buildings[4].rect.center[1]-self.y))                        
                elif buildings[4]!=0:
                    self.vector=pygame.math.Vector2(buildings[4].rect.center[0]-self.x,-(buildings[4].rect.center[1]-self.y))    
                self.unit_vector=pygame.math.Vector2.normalize(self.vector)
                projectile_speed_vector=10*self.unit_vector
                dx=projectile_speed_vector[0]
                dy=-projectile_speed_vector[1]
                x=self.rect.center[0]
                y=self.rect.center[1]
                projectiles.append(Projectile(x,y,dx,dy))
                self.shoot_timer=time.clock()+random.uniform(0.0,5.0)

        elif self.type==2:
            if time.clock()-self.shoot_timer>0.2:
                self.vector=pygame.math.Vector2(ship.x-self.x,-(ship.y-self.y))
                if ship.x>0 and ship.x<1020 and ship.y>0 and ship.alive==True:
                    a=random.randint(1,3)
                    if a<3:
                        self.vector=pygame.math.Vector2(ship.x-self.x,-(ship.y-self.y))
                    else:
                        self.vector=pygame.math.Vector2(buildings[4].rect.center[0]-self.x,-(buildings[4].rect.center[1]-self.y))                        
                elif buildings[4]!=0:
                    self.vector=pygame.math.Vector2(buildings[4].rect.center[0]-self.x,-(buildings[4].rect.center[1]-self.y))    
                self.unit_vector=pygame.math.Vector2.normalize(self.vector)
                projectile_speed_vector=10*self.unit_vector
                dx=projectile_speed_vector[0]
                dy=-projectile_speed_vector[1]
                x=self.rect.center[0]
                y=self.rect.center[1]
                projectiles.append(Projectile(x,y,dx,dy))
                self.shoot_timer=time.clock()+random.uniform(0.05,0.4)
        
       
    def random_spawn(self):
        if random.randint(1,2)==1:
            self.y=20-self.h
            self.x=random.randint(interface_x_left+50,interface_x_right-50)
            self.dx=random.uniform(-0.5,0.5)
            self.dy=random.uniform(0.1,0.5)
        else:
            if random.randint(1,2)==1:
                self.x=interface_x_left-self.w
                self.dx=random.uniform(0.1,0.5)
                self.dy=random.uniform(-0.5,0.5)

            else:
                self.x=interface_x_right
                self.dx=random.uniform(-0.5,-0.1)
            self.y=random.randint(interface_y_up,400)
            self.dy=random.uniform(-0.5,0.5)

        self.ingame=True
        print_message('>UFO sighted!',yellow)

def ufo_manager(quantity,delay):
    global spawn_timer
    global mission_completed
    n=0
    if len(ufot)+1<quantity:
        ufo_type=1
    else:
        ufo_type=2
        
    if time.clock()-spawn_timer>delay and len(ufot)+1<=quantity:
        ufot.append(Ufo(0,0,0,0,ufo_type))
        spawn_timer=time.clock()        

    for i in range(0,len(ufot)):
        if ufot[i]!=0:
            if ufot[i].ingame==False:
                ufot[i].random_spawn()
                ufot[i].ingame==True
            
            ufot[i].position(ufot[i].x,ufot[i].y,ufot[i].dx,ufot[i].dy)
            ufot[i].shoot()
            ufot[i].draw(ufot[i].x,ufot[i].y)
    for i in range(0,len(ufot)):
        if ufot[i]==0:
            n+=1
    if n==quantity:
        mission_completed=True

"""def ufo_test_simulation(quantity,delay):
    global spawn_timer
    
    if len(ufot)<quantity and time.clock()-spawn_timer>delay:
            ufot.append(Ufo(0,0,0,0))
            spawn_timer=time.clock()

    for i in range(0,len(ufot)):
        if ufot[i]!=0:
            if ufot[i].ingame==False:
                ufot[i].random_spawn()
                ufot[i].ingame==True
            ufot[i].position(ufot[i].x,ufot[i].y,ufot[i].dx,ufot[i].dy)
            if ship.alive==True:
                ufot[i].shoot()
            ufot[i].draw(ufot[i].x,ufot[i].y)
        if ufot[i]==0:
            ufot[i]=Ufo(0,0,0,0)    """
               
def collision_manager():

    global explosion_detail
    
    for i in range(len(ufot)):
        if ufot[i]!=0 and ship.alive==True:
            offset_x=ship.rect.center[0]-ufot[i].rect.center[0]
            offset_y=ship.rect.center[1]-ufot[i].rect.center[1]
            collide=ufot[i].mask.overlap(ship.mask,(offset_x,offset_y))
            if collide and ufot[i].can_collide==True:
                damage=0.05*math.sqrt((ship.dx-ufot[i].dx)**2+(ship.dy-ufot[i].dy)**2)*(ship.mass+ufot[i].mass)
                ship.hp+=-damage
                ship.hit_timer=time.clock()
                ufot[i].hp+=-damage
                create_explosion((ufot[i].x+ship.x)/2,(ufot[i].y+ship.y)/2,0,0,int(damage/3),0)
                temp_dx=ship.dx
                temp_dy=ship.dy
                ship.dx=0.8*ufot[i].dx/(ship.mass/ufot[i].mass)
                ship.dy=0.8*ufot[i].dy/(ship.mass/ufot[i].mass)
                ufot[i].colliding_dx=0.8*temp_dx/(ufot[i].mass/ship.mass)
                ufot[i].colliding_dy=0.8*temp_dy/(ufot[i].mass/ship.mass)
                ufot[i].colliding=True
                ufot[i].colliding_timer=time.clock()
                ufot[i].can_collide=False
                ufot[i].colliding_timer2=time.clock()
                if ship.hp<=0:
                    ship.dx=-ship.dx
                    ship.dy=-ship.dy
                if ufot[i].hp<=0:
                    create_debris(ufot[i].x,ufot[i].y,-ufot[i].dx,-ufot[i].dy,'light_grey',6)
                    create_explosion(ufot[i].x,ufot[i].y,-ufot[i].dx,-ufot[i].dy,explosion_detail,1)
                    ufot[i]=0
                    print_message('>UFO destroyed!',yellow)

        for j in range(len(ufot)):
            if ufot[j]!=0 and ufot[i]!=0 and j!=i:
                #ufot[i].mask.fill()
                #ufot[j].mask.fill()
                offset_x=ufot[j].rect.center[0]-ufot[i].rect.center[0]
                offset_y=ufot[j].rect.center[1]-ufot[i].rect.center[1]
                collide=ufot[i].mask.overlap(ufot[j].mask,(offset_x,offset_y))
                if collide and ufot[i].can_collide==True and ufot[j].can_collide==True:
                    damage=0.015*math.sqrt((ufot[j].dx-ufot[i].dx)**2+(ufot[j].dy-ufot[i].dy)**2)*(ufot[j].mass+ufot[i].mass)
                    ufot[i].hp+=-damage
                    ufot[j].hp+=-damage
                    create_explosion((ufot[i].x+ufot[j].x)/2,(ufot[i].y+ufot[j].y)/2,0,0,int(damage/3),0)
                    temp_dx=ufot[j].dx
                    temp_dy=ufot[j].dy
                    ufot[j].colliding_dx=0.8*ufot[i].dx/(ufot[j].mass/ufot[i].mass)
                    ufot[j].colliding_dy=0.8*ufot[i].dy/(ufot[j].mass/ufot[i].mass)
                    ufot[i].colliding_dx=0.8*temp_dx/(ufot[i].mass/ufot[j].mass)
                    ufot[i].colliding_dy=0.8*temp_dy/(ufot[i].mass/ufot[j].mass)
                    ufot[i].colliding=True
                    ufot[i].colliding_timer=time.clock()
                    ufot[i].can_collide=False
                    ufot[i].colliding_timer2=time.clock()
                    ufot[j].colliding=True
                    ufot[j].colliding_timer=time.clock()
                    ufot[j].can_collide=False
                    ufot[j].colliding_timer2=time.clock()

                    if ufot[i].hp<=0:
                        create_debris(ufot[i].x,ufot[i].y,-ufot[i].dx,-ufot[i].dy,'light_grey',6)
                        create_explosion(ufot[i].x,ufot[i].y,-ufot[i].dx,-ufot[i].dy,explosion_detail,1)
                        ufot[i]=0
                        print_message('>UFO destroyed!',yellow)

                    if ufot[j].hp<=0:
                        create_debris(ufot[j].x,ufot[j].y,-ufot[j].dx,-ufot[j].dy,'light_grey',6)
                        create_explosion(ufot[j].x,ufot[j].y,-ufot[j].dx,-ufot[j].dy,explosion_detail,1)
                        ufot[i]=0
                        print_message('>UFO destroyed!',yellow)

    
            for j in range(0,len(projectiles)):
                if projectiles[j]!=0 and ufot[i]!=0:
                    offset_x=projectiles[j].rect.center[0]-ufot[i].rect.center[0]
                    offset_y=projectiles[j].rect.center[1]-ufot[i].rect.center[1]
                    hit=projectiles[j].mask.overlap(ufot[i].mask,(offset_x,offset_y))
                    if hit:
                        damage=0.5*math.sqrt(projectiles[j].dx**2+projectiles[j].dy**2)*projectiles[j].mass
                        ufot[i].hp+=-damage
                        ufot[i].dx+=4*projectiles[j].mass/ufot[i].mass*projectiles[j].dx
                        ufot[i].dy+=4*projectiles[j].mass/ufot[i].mass*projectiles[j].dy
                        if damage>0:
                            create_explosion(projectiles[j].x,projectiles[j].y,0,0,int(damage/1.5),0)
                            projectiles[j]=0
                    
                        if ufot[i].hp<=0:
                            create_debris(ufot[i].x,ufot[i].y,ufot[i].dx,ufot[i].dy,'light_grey',6)
                            create_explosion(ufot[i].x,ufot[i].y,ufot[i].dx,ufot[i].dy,explosion_detail,1)
                            ufot[i]=0
                            print_message('>UFO destroyed!',yellow)
                            if 0<=random.randint(1,100)<=3:
                                print_message('>"Nice work, Captain!"',(comm_blue))
                            if 4<=random.randint(1,100)<=6:
                                print_message('>"Target down!"',(comm_blue))
                            if 7<=random.randint(1,100)<=10:
                                print_message('>"Well done!"',(comm_blue))
                            if 11<=random.randint(1,100)<=13:
                                print_message('>"Excellent work, Captain! Another one down."',(comm_blue))
                            if 14<=random.randint(1,100)<=16:
                                print_message('>"Hostile aircraft down, I repeat: hostile aircraft is down."',(comm_blue))
                            if 17<=random.randint(1,100)<=20:
                                print_message('>"Good job!"',(comm_blue))
                            if 21<=random.randint(1,100)<=24:
                                print_message('>"Yeah! Take that, you bastards!"',(comm_blue))
                            if 25<=random.randint(1,100)<=28:
                                print_message('>A fine hit, Captain!"."',(comm_blue))
                            if 28<=random.randint(1,100)<=30:
                                print_message('>Hit confirmed. The target is down."',(comm_blue))





                                
        
            for j in range(0,len(debris)):
                if debris[j]!=0 and ufot[i]!=0:
                    offset_x=debris[j].rect.center[0]-ufot[i].rect.center[0]
                    offset_y=debris[j].rect.center[1]-ufot[i].rect.center[1]
                    hit=debris[j].mask.overlap(ufot[i].mask,(offset_x,offset_y))
                    if hit:
                        damage=0.5*math.sqrt(debris[j].dx**2+debris[j].dy**2)*debris[j].mass
                        ufot[i].hp+=-damage
                        ufot[i].dx+=4*debris[j].mass/ufot[i].mass*debris[j].dx
                        ufot[i].dy+=4*debris[j].mass/ufot[i].mass*debris[j].dy
                        if damage>0:
                            create_explosion(debris[j].x,debris[j].y,0,0,int(damage/1.5),0)
                            debris[j]=0
                            if ufot[i].hp<=0:
                                create_debris(ufot[i].x,ufot[i].y,ufot[i].dx,ufot[i].dy,'light_grey',6)
                                create_explosion(ufot[i].x,ufot[i].y,ufot[i].dx,ufot[i].dy,explosion_detail,1)
                                ufot[i]=0
                                print_message('>UFO destroyed!',yellow)



            for j in range(0,len(projectiles)):
                if projectiles[j]!=0 and ship.hp>0:
                    offset_x=projectiles[j].rect.center[0]-ship.rect.center[0]
                    offset_y=projectiles[j].rect.center[1]-ship.rect.center[1]
                    hit=projectiles[j].mask.overlap(ship.mask,(offset_x,offset_y))
                    if hit:
                        damage=0.8*math.sqrt(projectiles[j].dx**2+projectiles[j].dy**2)*projectiles[j].mass
                        ship.hp+=-damage
                        ship.dx+=5*projectiles[j].mass/ship.mass*projectiles[j].dx
                        ship.dy+=5*projectiles[j].mass/ship.mass*projectiles[j].dy

                        if damage>0:
                            create_explosion(projectiles[j].x,projectiles[j].y,0,0,int(damage/1.5),0)
                            projectiles[j]=0
                            print_message('>Ship hit!',(255,40,40))
                            ship.hit_timer=time.clock()

            if ship.hp>0:
                for j in range(0,len(debris)):
                    if debris[j]!=0:
                        offset_x=debris[j].rect.center[0]-ship.rect.center[0]
                        offset_y=debris[j].rect.center[1]-ship.rect.center[1]
                        ship.mask.fill()
                        hit=debris[j].mask.overlap(ship.mask,(offset_x,offset_y))
                        if hit:
                            damage=0.8*math.sqrt(debris[j].dx**2+debris[j].dy**2)*debris[j].mass
                            ship.hp+=-damage
                            ship.hit_timer=time.clock()
                            ship.dx+=5*debris[j].mass/ship.mass*debris[j].dx
                            ship.dy+=5*debris[j].mass/ship.mass*debris[j].dy
                            create_explosion(debris[j].x,debris[j].y,0,0,int(damage/1.5),0)
                            debris[j]=0

    for i in range(0,len(buildings)):
        if buildings[i]!=0 and buildings[i].building_type!=alusta:
            for j in range(0,len(projectiles)):
                if projectiles[j]!=0 and buildings[i]!=0:
                    offset_x=projectiles[j].rect.center[0]-buildings[i].rect.center[0]
                    offset_y=projectiles[j].rect.center[1]-buildings[i].rect.center[1]
                    #hit=projectiles[j].mask.overlap(buildings[i].mask,(offset_x,offset_y))
                    
                    if abs(offset_x)<buildings[i].rect.width/2 and abs(offset_y)<buildings[i].rect.height/2:
                        damage=0.5*math.sqrt(projectiles[j].dx**2+projectiles[j].dy**2)*projectiles[j].mass
                        buildings[i].hp+=-damage
                        if damage>0:
                            create_explosion(projectiles[j].x,projectiles[j].y,0,0,int(damage/1.5),0)
                            projectiles[j]=0
                            if buildings[i].building_type==komentokeskus and random.randint(1,100)<=30:
                                print_message('>Command center under fire!',(255,40,40))
                            if buildings[i].hp<30 and random.randint(1,100)<15:
                                print_message('>"We are taking heavy damage down here, Captain. Protect the HQ at all costs!"',(120,120,255))
                    
                        if buildings[i].hp<=0:
                            create_debris(buildings[i].x,buildings[i].y,0,0,'light_grey',20)
                            create_explosion(buildings[i].rect.center[0],buildings[i].rect.center[1],0,0,explosion_detail,1)
                            buildings[i]=0
                 
            for j in range(0,len(debris)):
                if debris[j]!=0 and buildings[i]!=0:
                    offset_x=debris[j].rect.center[0]-buildings[i].rect.center[0]
                    offset_y=debris[j].rect.center[1]-buildings[i].rect.center[1]
                    hit=debris[j].mask.overlap(buildings[i].mask,(offset_x,offset_y))
                    if hit:
                        damage=0.5*math.sqrt(debris[j].dx**2+debris[j].dy**2)*debris[j].mass
                        buildings[i].hp+=-damage
                        if damage>0:
                            create_explosion(debris[j].x,debris[j].y,0,0,int(damage/1.5),0)
                            debris[j]=0
                    
                        if buildings[i].hp<=0:
                            create_debris(buildings[i].x,buildings[i].y,0,0,'light_grey',20)
                            create_explosion(buildings[i].rect.center[0],buildings[i].rect.center[1],0,0,explosion_detail,1)
                            buildings[i]=0

            for j in range(0,len(ufot)):
                if ufot[j]!=0 and buildings[i]!=0:
                    offset_x=buildings[i].rect.center[0]-ufot[j].rect.center[0]
                    offset_y=buildings[i].rect.center[1]-ufot[j].rect.center[1]
                    collide=ufot[j].mask.overlap(buildings[i].mask,(offset_x,offset_y))
                    if collide:
                        if math.sqrt(ufot[j].dx**2+ufot[j].dy**2)>0.5:
                            damage=(3*math.sqrt(ufot[j].dx**2+ufot[j].dy**2))**2*ufot[j].mass
                            building[i].hp+=-damage
                            ufo[j].hp+=-damage
                            create_explosion((ufot[j].x+buildings[i].x)/2,(ufot[j].y+buildings[i].y)/2,0,0,int(damage/3),0)
                            if buildings[i].hp<=0:
                                create_debris(buildings[i].x,buildings[i].y,0,0,'light_grey',20)
                                create_explosion(buildings[i].rect.center[0],buildings[i].rect.center[1],0,0,explosion_detail,1)
                                buildings[i]=0

                            if ufot[j].hp<=0:
                                create_debris(ufot[j].x,ufot[j].y,-ufot[j].dx,-ufot[j].dy,'light_grey',6)
                                create_explosion(ufot[j].x,ufot[j].y,-ufot[j].dx,-ufot[j].dy,explosion_detail,1)
                                ufot[j]=0
                                print_message('>UFO crashed!',yellow)

            if ship.alive==True and buildings[i]!=0:
                offset_x=buildings[i].rect.center[0]-ship.rect.center[0]
                offset_y=buildings[i].rect.center[1]-ship.rect.center[1]
                collide=ship.mask.overlap(buildings[i].mask,(offset_x,offset_y))
                damage=(math.sqrt(ship.dx**2+ship.dy**2))**2*ship.mass
                if collide:
                    if damage<1:
                        damage=0
                    if damage>0:
                        buildings[i].hp+=-0.3*damage
                        ship.hp+=-damage
                        create_explosion(ship.x,ship.y,0,0,int(damage/3),0)
                        ship.hit_timer=time.clock()
                        damage=0
                    if buildings[i].hp<=0:
                        create_debris(buildings[i].x,buildings[i].y,0,0,'light_grey',20)
                        create_explosion(buildings[i].x,buildings[i].y,0,0,explosion_detail,1)
                        buildings[i]=0
                elif ship.rect.bottom>=buildings[i].rect.top+7 and ship.dy>0 and buildings[i].rect.right>ship.rect.center[0]>buildings[i].rect.left:                
                    if math.sqrt(ship.dx**2+ship.dy**2)>2:
                        if damage<2:
                            damage=0
                        if damage>0:
                            buildings[i].hp+=-0.3*damage
                            ship.hp+=-damage
                            create_explosion(ship.x,ship.y,0,0,int(damage/3),0)
                            ship.hit_timer=time.clock()
                            damage=0
                        if buildings[i].hp<=0:
                            create_debris(buildings[i].x,buildings[i].y,0,0,'light_grey',20)
                            create_explosion(buildings[i].rect.center[0],buildings[i].rect.center[1],0,0,explosion_detail,1)
                            buildings[i]=0
                    ship.dy=0
                    ship.dx=0



def evasion_manager():
    for i in range(0,len(ufot)):
        if ufot[i]!=0:
            for j in range(0,len(ufot)):
                if ufot[j]!=0 and j!=i and ufot[i].evasion==True and ufot[j].evasion==True:
                    if abs(ufot[i].rect.center[0]-ufot[j].rect.center[0])<90 and abs(ufot[i].rect.center[1]-ufot[j].rect.center[1])<48:
                        if abs(ufot[i].rect.center[0]-ufot[j].rect.center[0])/90>abs(ufot[i].rect.center[1]-ufot[j].rect.center[1])/48:
                            ufot[i].dx=-0.1*ufot[i].dx
                        else:
                            ufot[i].dy=-0.1*ufot[i].dy
                        ufot[i].evasion=False
                        ufot[i].evasion_timer=time.clock()
global mission                                 
mission=1                                               #väliaikainen

def menu():
    Display.fill((0,0,0))
    
def event_handling():
    global ship
    global mission
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitGame = True
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                ship.dangle=2
                ship.thruster_left_on=True
            if event.key==pygame.K_RIGHT:
                ship.dangle=-2
                ship.thruster_right_on=True
            if event.key==pygame.K_DOWN:
                pass
            if event.key==pygame.K_UP:
                ship.thruster_on=True
            if event.key==pygame.K_SPACE:
                ship.shoots=True
                #ship.shoot()
            if event.key==pygame.K_r:
                mission1()
            if event.key==pygame.K_ESCAPE:
                pygame.quit()
                quit()
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_UP:
                ship.ddx=0
                ship.ddy=0
                ship.thruster_on=False
            if event.key==pygame.K_RIGHT:
                if ship.dangle==-2: 
                    ship.dangle=0
                    ship.thruster_right_on=False
            if event.key==pygame.K_LEFT:
                if ship.dangle==2:
                    ship.dangle=0
                    ship.thruster_left_on=False
            if event.key==pygame.K_SPACE:
                    ship.shoots=False

def build_level(mission):
    global ship
    global ufot
    global projectiles
    global buildings
    global explosion_particles
    global debris

    global r
    r=0
    global hp_warning
    hp_warning=False
    global temp_warning
    temp_warning=False

    global start_message_counter
    start_message_counter=0

    global console_lines
    console_lines=[]
    
    if mission==1:
        buildings=[]
        buildings.append(Building(paja,50,screen_h-ground_height-paja_h))
        buildings.append(Building(halli,320,screen_h-ground_height-halli_h))
        buildings.append(Building(halli,500,screen_h-ground_height-halli_h))
        buildings.append(Building(alusta,120,screen_h-ground_height-alusta_h))
        buildings.append(Building(komentokeskus,200,screen_h-ground_height-komentokeskus_h))
        buildings.append(Building(kerrostalo3,700,screen_h-ground_height-kerrostalo3_h))
        buildings.append(Building(kerrostalo2,825,screen_h-ground_height-kerrostalo2_h))
        buildings.append(Building(kerrostalo2,950,screen_h-ground_height-kerrostalo2_h))
        ship=Ship(120+alusta_w/2,screen_h-100-31/2+2,0,0,0,0,90,0)
        ufot=[]
        projectiles=[]
        debris=[]
        explosion_particles=[]

    if mission==2:
        buildings=[]
        buildings.append(Building(paja,50,screen_h-ground_height-paja_h))
        buildings.append(Building(halli,320,screen_h-ground_height-halli_h))
        buildings.append(Building(halli,500,screen_h-ground_height-halli_h))
        buildings.append(Building(alusta,120,screen_h-ground_height-alusta_h))
        buildings.append(Building(komentokeskus,200,screen_h-ground_height-komentokeskus_h))
        buildings.append(Building(kerrostalo3,700,screen_h-ground_height-kerrostalo3_h))
        buildings.append(Building(kerrostalo2,825,screen_h-ground_height-kerrostalo2_h))
        buildings.append(Building(kerrostalo2,950,screen_h-ground_height-kerrostalo2_h))
        ship=Ship(120+alusta_w/2,screen_h-100-31/2+2,0,0,0,0,90,0)
        ufot=[]
        projectiles=[]
        debris=[]
        explosion_particles=[]

global end_message
end_message=True

def end_mission():
    global end_message
    if mission==1:
        if end_message==True:
            print_message('>"Well done, Captain! We are not receiving any more hostile contacts. Return the ship safely to the launch pad for debriefing."',comm_blue)
            end_message=False
        if 120<ship.rect.center[0]<120+alusta_w and ship.rect.center[1]>=screen_h-100-31:
            mission2()

def mission1():
    
    global ufot
    global buildings
    global ship
    global mission_start
    global mission_completed
    global end_message
    end_message=True

    mission_completed=False
    mission_start=True
    ufot=[]

    shoot_timer=0
    ground_height=100

    time.clock()
    global spawn_timer
    spawn_timer=time.clock()

    build_level(1)

    pygame.draw.rect(Display, green, (0,screen_h-100,screen_w,100), 0)
    pygame.draw.rect(Display, bright_blue, (0,0,screen_w,screen_h-100), 0)

    global target_x
    global target_y
    
    target_x=buildings[4].rect.midtop[0]
    target_y=buildings[4].rect.midtop[1]   
    
    quitGame = False        
    while not quitGame:
        if mission_start==False:
            event_handling()
        
        pygame.draw.rect(Display, green, (0,screen_h-100,screen_w,100), 0)
        pygame.draw.rect(Display, bright_blue, (0,0,screen_w,screen_h-100), 0)

        draw_buildings()
        
        projectile_manager()
        debris_manager()
        explosion_manager()

        ufo_manager(5,18)
        #ufo_test_simulation(10,1)
        evasion_manager()
        if ship.alive==True:
            ship.position(ship.x,ship.y,ship.dx,ship.dy,ship.ddx,ship.ddy,ship.dangle)
                
            if ship.thruster_on==True:
                ship.thrust()
            if ship.shoots==True and time.clock()-shoot_timer>0.2:
                ship.shoot()
                shoot_timer=time.clock()
    
            ship.draw(ship.x,ship.y,ship.angle)

        collision_manager()
        draw_alusta()
        interface()
        if mission_completed==True:
            end_mission()
        pygame.display.update()

        clock.tick(60)

mission_list=[0,mission1(),mission2()]

def game():
    mission=1
    mission_list[mission]
    
game()
pygame.quit()
quit()
