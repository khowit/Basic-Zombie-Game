import pygame
pygame.init()

display_Width = 800
display_Height = 480

winDisplay = pygame.display.set_mode((display_Width, display_Height))
pygame.display.set_caption('Test Games')
clock = pygame.time.Clock()
bulletSound = pygame.mixer.Sound('image/bullet.mp3')
hitSound = pygame.mixer.Sound('image/hit.mp3')
music = pygame.mixer.music.load('image/music.mp3')
pygame.mixer.music.play(-1)

walkRight = [pygame.image.load('image/R1.png'), pygame.image.load('image/R2.png'), pygame.image.load('image/R3.png'), pygame.image.load('image/R4.png'), pygame.image.load('image/R5.png'), pygame.image.load('image/R6.png'), pygame.image.load('image/R7.png'), pygame.image.load('image/R8.png'), pygame.image.load('image/R9.png')]
walkLeft = [pygame.image.load('image/L1.png'), pygame.image.load('image/L2.png'), pygame.image.load('image/L3.png'), pygame.image.load('image/L4.png'), pygame.image.load('image/L5.png'), pygame.image.load('image/L6.png'), pygame.image.load('image/L7.png'), pygame.image.load('image/L8.png'), pygame.image.load('image/L9.png')]
bg = pygame.image.load('image/bg4.png')
char = pygame.image.load('image/standing.png')

class player():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 10
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def draw(self,winDisplay):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if not(self.standing):
            if self.left:
                winDisplay.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                winDisplay.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
        else:
            if self.right:
                winDisplay.blit(walkRight[0], (self.x,self.y))
            else:
                winDisplay.blit(walkLeft[0], (self.x,self.y))

        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        # pygame.draw.rect(winDisplay, (255,0,0), self.hitbox, 2)
    
    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 64
        self.y = 328 
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255,0,0))
        winDisplay.blit(text, (250 - (text.get_width()/2), 200))
        pygame.display.update()
        i = 0
        while i < 200:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()
        
class projectile():
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing
    
    def draw(self, winDisplay):
        pygame.draw.circle(winDisplay, self.color, (self.x, self.y), self.radius)
       

class enemy():
    walkRight = [pygame.image.load('image/R1E.png'), pygame.image.load('image/R2E.png'), pygame.image.load('image/R3E.png'), pygame.image.load('image/R4E.png'), pygame.image.load('image/R5E.png'), pygame.image.load('image/R6E.png'), pygame.image.load('image/R7E.png'), pygame.image.load('image/R8E.png'), pygame.image.load('image/R9E.png'), pygame.image.load('image/R10E.png'), pygame.image.load('image/R11E.png')]
    walkLeft = [pygame.image.load('image/L1E.png'), pygame.image.load('image/L2E.png'), pygame.image.load('image/L3E.png'), pygame.image.load('image/L4E.png'), pygame.image.load('image/L5E.png'), pygame.image.load('image/L6E.png'), pygame.image.load('image/L7E.png'), pygame.image.load('image/L8E.png'), pygame.image.load('image/L9E.png'), pygame.image.load('image/L10E.png'), pygame.image.load('image/L11E.png')]
    
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True

    def draw(self, winDisplay):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                winDisplay.blit(self.walkRight[self.walkCount //3], (self.x, self.y))
                self.walkCount += 1
            else:
                winDisplay.blit(self.walkLeft[self.walkCount //3], (self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(winDisplay, (255,0,0), (self.hitbox[0],self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(winDisplay, (140,255,0), (self.hitbox[0],self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x + 17, self.y + 2, 37, 57)
            # pygame.draw.rect(winDisplay, (255,0,0), self.hitbox, 2)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print('hit')
     

def main():
    score = 0
    def raedrawGameWindown():
        winDisplay.blit(bg,(0,0))
        text = font.render('Score : '+ str(score), 1, (255,255,255))
        winDisplay.blit(text, (600,10))
        man.draw(winDisplay)
        goblin.draw(winDisplay)

        for bullet in bullets:
            bullet.draw(winDisplay)
        pygame.display.update()
    
    font = pygame.font.SysFont('comicsans', 25, True)
    man = player(400,328,64,64)
    goblin = enemy(100, 333, 64, 64, 700)
    shootLoop = 0
    bullets = []
    run = True
    while run:
        clock.tick(30)
        if goblin.visible == True:
            if man.hitbox[1] < goblin.hitbox[1]+goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
                if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                    man.hit()
                    score -= 5

        if shootLoop > 0:
            shootLoop += 1
        if shootLoop > 3:
            shootLoop = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
        for bullet in bullets:
            if bullet.y - bullet.radius < goblin.hitbox[1]+goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
                if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                    goblin.hit()
                    hitSound.play()
                    score += 1
                    bullets.pop(bullets.index(bullet))

            if bullet.x < 800 and bullet.x > 0 :
                bullet.x += bullet.vel
            else:
                bullets.pop(bullets.index(bullet))
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and shootLoop == 0:
            bulletSound.play()
            if man.left:
                facing = -1
            else:
                facing = 1

            if len(bullets) < 5:
                bullets.append(projectile(round(man.x + man.width//2), round(man.y + man.height//2), 10, (255,255,0), facing))

            shootLoop = 1

        if keys[pygame.K_LEFT] and man.x > man.vel:
            man.x -= man.vel
            man.left = True
            man.right = False
            man.standing = False

        elif keys[pygame.K_RIGHT] and man.x < 800 - man.width - man.vel:
            man.x += man.vel
            man.right = True
            man.left = False
            man.standing = False
            
        else:
            man.standing = True
            man.walkCount = 0

        if not(man.isJump):
            if keys[pygame.K_UP]:
                man.isJump = True
        else:
            if man.jumpCount >= -10:
                neg = 1
                if man.jumpCount < 0:
                    neg = -1
                man.y -= (man.jumpCount ** 2)*0.5*neg
                man.jumpCount -= 1
            else:
                man.isJump = False
                man.jumpCount = 10

        raedrawGameWindown()

    pygame.quit()
    quit()

if __name__ == "__main__":
    main()
