import pygame, os, random
import game_module as gm
from pygame import mixer


os.environ['SDL_VIDEO_CENTERED'] = '1'  # centrowanie okna
pygame.init()
WIDTH, HEIGHT = 1366, 740

## ustawienia ekranu i gry
screen = pygame.display.set_mode(gm.SIZESCREEN)
pygame.display.set_caption('Space Invaders')
clock = pygame.time.Clock()
path1 = os.path.join(os.pardir, 'sounds')

background_path = os.path.join(path1, "background.wav")
win_path = os.path.join(path1, "win.wav")
lose_path = os.path.join(path1, "lose.wav")
shoot_path = os.path.join(path1, "shoot.wav")
ugh_path = os.path.join(path1, "ugh.wav")

backMusic = mixer.Sound(background_path)
backMusic.play(-1)


# klasa gracza
class Player(pygame.sprite.Sprite): #konstruktor
    def __init__(self, file_image, x, y):
        super().__init__()
        self.image = file_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.kills = 0
        self.lives = 1

    def draw(self, surface): #ryswoanie gracza
        surface.blit(self.image, (self.x, self.y))

    def detect_collision(self):  #sprawdzanie kolizji dla gracza
        for bullet in enemy_bullets:
            if (bullet.x > self.x and bullet.x < self.x + 73
                    and bullet.y > self.y and bullet.y < self.y + 52):
                enemy_bullets.remove(bullet)
                self.lives -= 1

                # jeden warunek na przegrana
                if self.lives <= 0:
                    self.lives = 0
                    lose_sound = mixer.Sound(lose_path)
                    lose_sound.play()
                    enemies.clear()
                    enemy_bullets.clear()
                    shields.clear()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, file_image, image_list, x, y): #konstruktor
        super().__init__()
        self.image = file_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.image_list = image_list
        self._count = 0
        self._count1 = 0
        self._count2 = 0
        self.lives = 1
        self.movement = True

    def draw(self, surface):  #ryswoanie przeciwnika
        surface.blit(self.image, (self.x, self.y))
        self.y += 0.1

    def update(self): #ryswoanie przeciwnika
        if self.movement:
            if self.y > 0:
                self._move(self.image_list)
        if self.lives <= 0:
            self.movement = False
            self._death(self.image_list)

    def _move(self, image_list): #animacja przeciwnika
        if self._count < 20:
            self.image = image_list[0]
        elif self._count < 40:
            self.image = image_list[1]

        if self._count < 40:
            self._count += 1
        else:
            self._count = 0

    def _death(self, image_list): #animacja dla śmierci przeciwnika
        if self._count2 < 1:
            ugh_sound = mixer.Sound(ugh_path)
            ugh_sound.play()
        if self._count2 < 10:
            self.image = image_list[2]

        if self._count2 < 30:
            self._count2 += 1
        else:

            enemies.remove(self)
            self._count2 = 0

    def shoot(self, choseEnemy): #tworzenie nowego obiektu jakim jest pocisk przeciwnika
        if self._count1 < 1:
            enemy_bullets.append(Enemy_Bullet(gm.ENEMY_BULLET, choseEnemy.x + 29, choseEnemy.y))

        if self._count1 < 100:
            self._count1 += 1
        else:
            self._count1 = 0

    def detect_collision(self): #sprawdzanie kolizji dla przeciwnika
        for bullet in bullets:
            if self.movement:
                if (bullet.x > self.x and bullet.x < self.x + 110
                        and bullet.y > self.y and bullet.y < self.y + 80):
                    bullets.remove(bullet)
                    self.lives -= 1
                    player.kills += 1

                    # warunek na wygrana
                    if player.kills >= 30:
                        win_sound = mixer.Sound(win_path)
                        win_sound.play()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, file_image, x, y): #konstruktor
        super().__init__()
        self.image = file_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def draw(self, surface): #rysowanie pocisku gracza
        surface.blit(self.image, (self.x, self.y))
        self.y -= 4

    def _delete_bullets(self): #usuwanie pocisku gracza gdy ten wyleci poza ekran gry
        for bullet in bullets:
            if bullet.y < 0:
                bullets.remove(bullet)
                print(len(bullets))


class Enemy_Bullet(Bullet): #klasa pocisku przeciwnika dziedziczona po pocisku gracza
    def __init__(self, file_image, x, y): #konstruktor
        super().__init__(file_image, x, y)

    def draw(self, surface): #rysowanie pocisku przeciwnika
        surface.blit(self.image, (self.x, self.y))
        self.y += 3

    def _delete_bullets(self): #usuwanie pocisku przeciwnika gdy ten wyleci poza ekran gry
        for bullet in enemy_bullets:
            if bullet.y > gm.HEIGHT + 100:
                enemy_bullets.remove(bullet)


class Shield(Enemy):
    def __init__(self, start_image, image_list, x, y):
        super().__init__(start_image, image_list, x, y)
        self.lives = 2
        self.count3 = 0

    def draw(self, surface):  # rysowanie pocisku przeciwnika
        surface.blit(self.image, (self.x, self.y))
        if self.count3 < 50:
           self.x += 2
        if self.count3 >50:
           self.x -= 2

        if self.count3 < 100:
            self.count3 += 1
        else:
            self.count3 = 0

    def _move(self, image_list):
        if self.lives==2:
            self.image = image_list[0]
        if self.lives == 1:
            self.image = image_list[1]
        if self.lives <=0:
            shields.remove(self)

    def detect_collision(self):
        for bullet in bullets:
            if self.movement:
                if (bullet.x > self.x and bullet.x < self.x + 123
                        and bullet.y > self.y and bullet.y < self.y + 57):
                    bullets.remove(bullet)
                    self.lives -= 1



# class Enemy2(Enemy):
#  def __init__(self, start_image, image_list, x, y):
#       super().__init__(start_image, image_list, x, y)


# konkretyzacja obiektów

player = Player(gm.PLAYER, WIDTH / 2 - 50, 600)

enemies = []
bullets = []
enemy_bullets = []
shields = []

#tworzenie 30 przeciwnikow
for x in range(1, 11):
    for y in range(1, 2):
        enemies.append(Enemy(gm.EN1_1, gm.ENEMY_LIST, x * 120 - 40, y * 90))
    for y in range(1, 2):
        enemies.append(Enemy(gm.EN2_1, gm.ENEMY_LIST2, x * 120 - 30, 2 * y * 90))
    for y in range(1, 2):
        enemies.append(Enemy(gm.EN1_1, gm.ENEMY_LIST3, x * 120 - 40, 3 * y * 90))

for x in range (1,5):
    shields.append(Shield(gm.SH1, gm.SHIELD_LIST, x * 300 - 150, 5*y * 90))

# koncowy label
def Endwindow(text, flag):
    font = pygame.font.SysFont('', 150)
    message = font.render(text, False, (0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), (0, 200, 1366, 300))
    screen.blit(message, (370, 300))

    #flag1=przegrana     flag2=wygrana
    if flag == 1:
        pygame.draw.rect(screen, (255, 255, 255), (0, 200, 1366, 300))
        screen.blit(message, (370, 300))
    if flag == 2:
        pygame.draw.rect(screen, (255, 255, 255), (0, 200, 1366, 300))
        screen.blit(message, (500, 300))


# głowna pętla gry
window_open = True
while window_open:

    # sterowanie
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:  # ruch w lewo
        if player.x > 20:
            player.x -= 6
    if keys[pygame.K_RIGHT]:  # ruch w prawo
        if player.x < WIDTH - 140:
            player.x += 6

    screen.blit(gm.BACKGROUND, (0, -50))
    # pętla zdarzeń
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            window_open = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP: #event odpowiedzialny za strzelanie
            bullets.append(Bullet(gm.BULLET, player.x + 29, player.y))
            bullet_sound = mixer.Sound(shoot_path)
            bullet_sound.play()

    # rysowanie i aktualizacja obiektów

    if len(enemies) > 0:
        choseEnemy = random.choice(enemies) #wybieranie losowego enemy potrzebne do metody shoot
    for enemy in enemies: #metody dla przeciwnika
        enemy.update()
        enemy.draw(screen)
        enemy.detect_collision()
        enemy.shoot(choseEnemy)

    for shield in shields:
        shield.update()
        shield.draw(screen)
        shield.detect_collision()

    for bullet in bullets: #metody dla kul gracza
        bullet.draw(screen)
        bullet._delete_bullets()

    for bullet in enemy_bullets: #metody dla kul przeciwnika
        bullet.draw(screen)
        bullet._delete_bullets()

    player.draw(screen) #rysowanie gracza
    player.detect_collision()

    # rysowanie ilości życia i zabojstw
    font = pygame.font.Font(None, 30)
    text = font.render("LIVES = ", False, (255, 255, 255))
    text1 = font.render(str(player.lives), False, (255, 255, 255))
    screen.blit(text, (20, 10))
    screen.blit(text1, (100, 10))

    font = pygame.font.Font(None, 30)
    text = font.render("KILLS = ", False, (255, 255, 255))
    text1 = font.render(str(player.kills), False, (255, 255, 255))
    screen.blit(text, (20, 30))
    screen.blit(text1, (100, 30))

# wyskakuje oknokoncowe po spelnieniu odpowiednich warunkow
    if len(enemies) <= 0: #wygrana - zabicie wszystkich
        Endwindow("You win", 2)
        backMusic.stop()

    if player.lives <= 0: #przegrana - koniec życia
        Endwindow("Game Over", 1)
        backMusic.stop()

    if enemy.y > HEIGHT - 220: #przegrana - przeciwnik w za małej odległości
        Endwindow("Game Over", 1)
        backMusic.stop()
        enemy_bullets.clear()

# aktualizacja okna pygame
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
