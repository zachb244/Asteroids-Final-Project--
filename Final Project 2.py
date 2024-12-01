from mimetypes import inited

import pygame
import math
import random #used for asteroids
pygame.init()

width=800
height=800

#imports images into pygame (some taken from video for size reasons)
background = pygame.image.load('Space-y Sprites/background2.png')
ship = pygame.image.load('Space-y Sprites/spaceRocket.png')
asteroid50 = pygame.image.load('Space-y Sprites/asteroid50.png')
asteroid100 = pygame.image.load('Space-y Sprites/Medium Asteroid PNG.png')
asteroid150 = pygame.image.load('Space-y Sprites/big asteroid.png')

#declares the display
win=pygame.display.set_mode((width, height))
pygame.display.set_caption('Space-y')

#sets the clock
clock = pygame.time.Clock()

gameover = False
lives = 3
score = 0

#Class for user ship
class Ship(object):
    def __init__(self):
        #Defines the actual object
        self.img = ship
        self.width = self.img.get_width()
        self.height = self.img.get_height()

        #Gives ship an (x,y) position on the window
        self.x = width//2
        self.y = height//2
        self.angle = 0

        #Accounts for ship movement/turning (I have no alternative code for this method had to copy the video)
        self.rotatedShip = pygame.transform.rotate(self.img, self.angle)
        self.rotatedWindow = self.rotatedShip.get_rect()
        self.rotatedWindow = (self.x, self.y)

        #Accounts for ship turning specifically (Had to copy video/ let python fill in, this is way beyond my abilities lol)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))

        #Tracks location of front of ship(for bullet functionality)
        self.front = (self.x + self.cosine * self.width//2, self.y - self.sine * self.height//2)


    #Displays ship in game window
    def displayShip(self,window):
        window.blit(self.rotatedShip, self.rotatedWindow)

    # Functions for turning (same structure copied to all)
    def left(self):
        self.angle += 5 #speed of turn
        self.rotatedShip = pygame.transform.rotate(self.img, self.angle)
        self.rotatedWindow = self.rotatedShip.get_rect()
        self.rotatedWindow.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        # Resets the self.front argument so that it updates in accordance with the ship's turning (python filled in/ video)
        self.front = (self.x + self.cosine * self.width//2, self.y - self.sine * self.height//2)

    def right(self):
        self.angle -= 5
        self.rotatedShip = pygame.transform.rotate(self.img, self.angle)
        self.rotatedWindow = self.rotatedShip.get_rect()
        self.rotatedWindow.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.front = (self.x + self.cosine * self.width//2, self.y - self.sine * self.height//2)

    def forward(self):
        self.x += self.cosine * 6 #Ship Move speed
        self.y -= self.sine * 6 #Ship Move speed
        self.rotatedShip = pygame.transform.rotate(self.img, self.angle)
        self.rotatedWindow = self.rotatedShip.get_rect()
        self.rotatedWindow.center = (self.x, self.y) #possible talking point (movement is not smooth without the .center appended to self.rotatedWindow)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.front = (self.x + self.cosine * self.width//2, self.y - self.sine * self.height//2)

#bullet class

class Bullets(object):
    def __init__(self):
        self.barrel = userShip.front #uses self function defined earlier that tracks the front of the ship
        self.x, self.y = self.barrel
        self.width = 4
        self.height = 4
        #tracks cosine and sine of player to determine which direction to shoot bullet
        self.cosine= userShip.cosine
        self.sine= userShip.sine
        # Bullet Velocity
        self.xvelocity = self.cosine * 10  # 10x the speed of the ship
        self.yvelocity = self.sine * 10

    # Updates bullet position on the screen
    def bulletMove(self):
        self.x += self.xvelocity
        self.y -= self.yvelocity

    #bullet display function
    def draw(self,win):
        pygame.draw.rect(win, (255,255,255), (self.x, self.y, self.width, self.height))

#Asteroid Class
class Asteroids(object):
    def __init__(self, rank):
        #determines which size asteroid is entering the screen
        self.rank = rank
        if rank == 1:
            self.image = asteroid50
        elif rank == 2:
            self.image = asteroid100
        else:
            self.image = asteroid150
        self.width = 50 * rank
        self.height = 50 * rank
        #How the asteroid enters the screen
        self.ranPoint = random.choice([(random.randrange(0, width - self.width), random.choice([-1 * self.height - 5, height +5])),(random.choice([-1 * self.width - 5, width +5]), random.randrange(0, height -self.height))])
        self.x, self.y = self.ranPoint
        if self.x < width//2:
            self.xdirection =1
        else:
            self.xdirection =-1
        if self.y < height//2:
            self.ydirection = 1
        else:
            self.ydirection = -1
        self.xvelocity = self.xdirection *random.randrange(1,3)
        self.yvelocity = self.ydirection *random.randrange(1,3)

    def draw(self,win):
        win.blit(self.image, (self.x, self.y))


#Actually displays the code on screen
def redrawWindow():
    win.blit(background, (0, 0))
    font = pygame.font.SysFont('comicsans', 30)
    livestext = font.render('Lives: ' + str(lives), 1, (0,128,0))
    scoretext = font.render('Score: ' + str(score), 1, (0,128,0))
    playagaintext = font.render('Press space to play again', 1, (0,128,0))
    #displays the ship
    userShip.displayShip(win)
    #displays asteroids
    for a in asteroids:
        a.draw(win)
    #displays the bullets
    for b in userBullets:
        b.draw(win)
    win.blit(livestext,(25,25))
    win.blit(scoretext,(25,75))
    if gameover:
        win.blit(playagaintext,(250,400))

    #Constantly updates game window
    pygame.display.update()


#PRIMARY WHILE LOOP
userShip = Ship()
userBullets =[]
asteroids= []
time = 0

run = True
while run:
    clock.tick(60)
    time += 1
    if not gameover:
        #Randomly selects asteroid rank based on amount of time passed
        if time % 50 == 0:
            ran = random.choice([1,1,1,2,2,3])
            asteroids.append(Asteroids(ran))

        #Update asteroid velocity
        for a in asteroids:
            a.x += a.xvelocity
            a.y += a.yvelocity

        #loops through asteroids and checks to see if player was hit
            if (a.x <= userShip.x <= a.x + a.width) or (a.x <= userShip.x + userShip.width <= a.x + a.width): #if these return true, player has collided with asteroid
                if (a.y <= userShip.y <= a.y + a.height) or (a.y <= userShip.y + userShip.height <= a.y + a.height):
                    lives -= 1
                    asteroids.pop(asteroids.index(a))
                    break #stops from continuously checking if hit

            #check for collisions
            for b in userBullets:
                if a.x <= b.x <= a.x + a.width or a.x <= b.x + b.width <= a.x + a.width: #Checks if bullet is on side of asteroids
                    if a.y <= b.y <= a.y + a.height or b.y +b.height >= a.y and b.y + b.height<= a.y + a.height: #Checks if bullet is on top or bottom of asteroid
                        if a.rank == 3:
                            score += 30
                        elif a.rank == 2:
                            score += 20
                        else:
                            score += 10
                        asteroids.pop(asteroids.index(a))
                        userBullets.pop(userBullets.index(b))



        #updates bullet position
        for b in userBullets:
            b.bulletMove()

        if lives <= 0:
            gameover = True


        #Applies Key presses to movement functions
        movement = pygame.key.get_pressed()
        if movement [pygame.K_LEFT]:
            userShip.left()
        if movement [pygame.K_RIGHT]:
            userShip.right()
        if movement [pygame.K_UP]:
            userShip.forward()





    #checks if game has ended
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Bullet Keypress is in this for loop so it is not continuously called on one keypress
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not gameover:
                    userBullets.append(Bullets())
                else:
                    gameover = False
                    score = 0
                    lives = 3
                    asteroids.clear()


    redrawWindow()
pygame.quit()