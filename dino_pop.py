from dino import *
from neuron import *
import pygame
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 550
WINDOW_SIZE = [WINDOW_WIDTH, WINDOW_HEIGHT]

class Dino_population:
    def __init__(self,PopNumber,id=1,prevPop=[]):
        self.PopNumber=PopNumber
        self.id=id
        self.brains=Population(self.PopNumber,[3,4,3,3],prevPop)
        self.population=[]
        for i in self.brains.population:
            self.population.append(Dino(i))
        self.score=0
        self.lastCactus=-600
        self.still_alive=self.PopNumber
        self.records=[]

        self.dots = []
        self.cactuses = [400,700]

        while True:
            self.score += 1
            KeysPressed = pygame.key.get_pressed()
            UP = KeysPressed[pygame.K_UP]
            DOWN = KeysPressed[pygame.K_DOWN]

            if UP:
                self.population[0].jump()
            elif DOWN:
                self.population[0].down()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.show()
            pygame.display.flip()
            if not self.move_all():
                break
            self.lastCactus += 1+self.score//1000
            last_cactus = self.add_random_elements()
            clock.tick(70)

        self.new_pop()

    def show(self):
        global screen, WINDOW_HEIGHT, dino_image, cactus_image, big_font, small_font, high_score, dino_image_best

        screen.fill((255, 255, 255))

        # Info Text
        text = big_font.render("Generation: "+str(self.id)+'  Score: '+str(self.score),True, (0,0,0))
        screen.blit(text, (50,50))

        text = big_font.render("High score: "+str(high_score)+"  Alive: "+str(self.still_alive), True, (0, 0, 0))
        screen.blit(text, (50, 80))

        #Ground line
        pygame.draw.line(screen, [0,0,0], (10, WINDOW_HEIGHT-40), (900, WINDOW_HEIGHT-40),2)

        #Graph
        pygame.draw.line(screen, [0,0,0], (500, 200), (700, 200),2)
        pygame.draw.line(screen, [0, 0, 0], (500, 50), (500, 200), 2)

        pygame.draw.rect(screen,[255,0,0], pygame.Rect(525,200,50,self.distance_nearest_cactus()*-100))
        text=small_font.render("Distance nearest",True,[0,0,0])
        screen.blit(text, (515, 210))

        pygame.draw.rect(screen,[64, 255, 0], pygame.Rect(600,200,50,self.score/-300))
        text = small_font.render("Speed", True, [0, 0, 0])
        screen.blit(text, (615, 210))
        #Show the Dinos
        for i in range(len(self.population)):
            dino=self.population[i]
            if dino.alive:
                if self.id!=1 and i<=4:
                    screen.blit(dino_image_best, (60, WINDOW_HEIGHT-dino.y-50-40))
                else:
                    screen.blit(dino_image, (60, WINDOW_HEIGHT-dino.y-50-40))

        #Show cactuses and dots
        for i in self.cactuses:
            screen.blit(cactus_image, (i, WINDOW_HEIGHT-40-40))

        for x,y in self.dots:
            pygame.draw.line(screen, [0,0,0], (x,WINDOW_HEIGHT+y-40), (x,WINDOW_HEIGHT+y-40),5)

    def move_all(self):
        distance_nearest=self.distance_nearest_cactus()
        for i in self.population:
            if i.alive:
                i.move(distance_nearest,self.score)

        deleted=0
        for a in range(len(self.cactuses)):
            i=a-deleted
            self.cactuses[i]-=(3+self.score//1000)
            if self.cactuses[i]<20:
                self.cactuses.pop(0)
                deleted+=1
            elif self.cactuses[i]<=100:
                for dino in self.population:
                    if dino.alive:
                        if dino.y<=40:
                            dino.dead()
                            self.records.append((dino.brain,self.score))
                            self.still_alive-=1

        deleted = 0
        for a in range(len(self.dots)):
            i = a - deleted
            self.dots[i][0]-=(3+self.score//1000)
            if self.dots[i][0]<0:
                self.dots.pop(0)
                deleted += 1

        if self.still_alive==0:
            return False
        return True

    def add_random_elements(self):
        if self.lastCactus>300:
            if random.randint(0,100)<=10:
                self.cactuses.append(900-50)
                self.lastCactus=0
        elif self.score in {0,100,250,350,500,750}:
            self.cactuses.append(900 - 50)

        if random.randint(0,3)==0:
            self.dots.append([900,random.randint(1,10)])
    def distance_nearest_cactus(self):
        if len(self.cactuses)>=1:
            return 1-self.cactuses[0]/850
        else:
            return 0

    def sort(self,lis, leng):
        sample = lis[::-1]
        sortd = []
        num = 0
        pre = -1
        for obj, score in sample:
            if score != pre:
                pre = score
                sortd.append((obj, score // 100))
                num += 1
                if num == leng:
                    return sortd
        return sortd

    def new_pop(self):
        global pop, high_score
        high_score=max(high_score,self.score)
        next_models=self.sort(self.records,5)
        pop=Dino_population(self.PopNumber,self.id+1,next_models)

# -----------------------------------------------------------------------------------------------
pygame.init()
#WINDOW_WIDTH = pygame.display.Info().current_w
#WINDOW_HEIGHT = pygame.display.Info().current_h



screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Dino AI")

big_font = pygame.font.Font('freesansbold.ttf', 20)
small_font = pygame.font.SysFont('calibri', 10)
cactus_image = pygame.transform.scale(pygame.image.load(r'cactus.png'),(40,40))
dino_image = pygame.transform.scale(pygame.image.load(r'Dinausaure.png'),(50,50))
dino_image_best = pygame.transform.scale(pygame.image.load(r'Dinausaure_blue.png'),(50,50))

high_score=0
clock = pygame.time.Clock()
# --------------------------------------------------------------------------------------------------

pop=Dino_population(100)
