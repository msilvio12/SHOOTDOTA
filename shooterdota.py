import pygame, random

WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = (0, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter")
clock = pygame.time.Clock()

def draw_text(surface, text, size, x, y):
	font = pygame.font.SysFont("serif", size)
	text_surface = font.render(text, True, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surface.blit(text_surface, text_rect)

def draw_shield_bar(surface, x, y, percentage):
	BAR_LENGHT = 100
	BAR_HEIGHT = 20
	fill = (percentage / 100) * BAR_LENGHT
	border = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
	fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
	pygame.draw.rect(surface, GREEN, fill)
	pygame.draw.rect(surface, WHITE, border, 2)

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("assets/player.png").convert()
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH // 2
		self.rect.bottom = HEIGHT - 10
		self.speed_x = 0
		self.shield = 100 #ESCUDO DE VIDA

	def update(self):
		self.speed_x = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.speed_x = -5
		if keystate[pygame.K_RIGHT]:
			self.speed_x = 5
		self.rect.x += self.speed_x
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0

	def shoot(self):
		bullet = Bullet(self.rect.centerx, self.rect.top)
		all_sprites.add(bullet)
		bullets.add(bullet)
		laser_sound.play()

class Meteor(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = random.choice(meteor_images)
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = random.randrange(-140, -100)
		self.speedy = random.randrange(1, 20)#velocidad de los meteoros
		self.speedx = random.randrange(-5, 5)#direccion de los meteoros

	def update(self):
		self.rect.y += self.speedy
		self.rect.x += self.speedx
		if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 25:
			self.rect.x = random.randrange(WIDTH - self.rect.width)
			self.rect.y = random.randrange(-100, - 40)
			self.speedy = random.randrange(1, 10)

class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.image.load("assets/laser1.png")
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.centerx = x
		self.speedy = -10

	def update(self):
		self.rect.y += self.speedy
		if self.rect.bottom < 0:
			self.kill()

class Explosion(pygame.sprite.Sprite):
	def __init__(self, center):
		super().__init__()
		self.image = explosion_anim[0]
		self.rect = self.image.get_rect()
		self.rect.center = center 
		self.frame = 0
		self.last_update = pygame.time.get_ticks()
		self.frame_rate = 50 # VELOCIDAD DE LA EXPLOSION

	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > self.frame_rate:
			self.last_update = now
			self.frame += 1
			if self.frame == len(explosion_anim):
				self.kill()
			else:
				center = self.rect.center
				self.image = explosion_anim[self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center
    


# Función para dibujar texto con color y bordes

def draw_text_with_border(surface, text, size, x, y, color, border_color):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    border_rect = pygame.Rect(text_rect.left - 2, text_rect.top - 2, text_rect.width + 4, text_rect.height + 4)
    pygame.draw.rect(surface, border_color, border_rect)
    surface.blit(text_surface, text_rect)

def show_go_screen():
    screen.blit(background, [0,0])
    draw_text_with_border(screen, "SHOOTER 2", 110, WIDTH // 2, HEIGHT // 4, (255, 255, 0), (0, 0, 0))
    draw_text_with_border(screen, "PUEDES HACER 1000 PUNTOS?", 50, WIDTH // 2, HEIGHT // 2, (255, 255, 0), (0, 0, 0))
    draw_text_with_border(screen, "ESTAS LISTO?", 40, WIDTH // 2, HEIGHT * 3/4, (255, 255, 0), (0, 0, 0))
    draw_text_with_border(screen, "PRESIONA UNA TECLA", 35, WIDTH // 2, HEIGHT * 3/4 + 60, (255, 255, 0), (0, 0, 0))
    #draw_text_with_border(screen, "SHOOTER 2", 65, WIDTH // 2, HEIGHT // 4, (255, 255, 0), (0, 0, 0))
    #draw_text_with_border(screen, "ESTAS LISTO?", 27, WIDTH // 2, HEIGHT // 2, (255, 255, 0), (0, 0, 0))
    #draw_text_with_border(screen, "Presiona una tecla", 20, WIDTH // 2, HEIGHT * 3/4, (255, 255, 0), (0, 0, 0))
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

def show_game_over_screen():
    screen.fill((0, 0, 0))
    draw_text_with_border(screen, "PERDISTE!!! FRACASADO!!!", 40, WIDTH // 2, HEIGHT // 2, (255, 255, 0), (0, 0, 0))
    pygame.display.flip()
    pygame.time.wait(2000)


meteor_images = []
meteor_list = ["assets/meteorGrey_big1.png","assets/meteorGrey_big4.png","assets/meteorGrey_small1.png", "assets/meteorGrey_med1.png"]
for img in meteor_list:
    meteor_images.append(pygame.image.load(img).convert())

#----------------EXPLOSION IMAGENES --------------

explosion_anim = []
for i in range(0, 2):
    file = "assets/regularExplosion0{}.png".format(i)
    img = pygame.image.load(file).convert()
    img.set_colorkey(BLACK)
    img_scale = pygame.transform.scale(img, (70,70))
    explosion_anim.append(img_scale)

# CARGAR IMAGENES DE FONDO
background = pygame.image.load("assets/nebulosa-via-lactea.png").convert()

# CARGAR SONIDOS
laser_sound = pygame.mixer.Sound("assets/laser5.ogg")
explosion_sound = pygame.mixer.Sound("assets/explosion.ogg")
pygame.mixer.music.load("assets/boss.ogg")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(loops=-1)

#### ----------GAME OVER
game_over = True
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        meteor_list = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            meteor = Meteor()
            all_sprites.add(meteor)
            meteor_list.add(meteor)
        score = 0

    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    all_sprites.update()

    # colisiones - meteoro - laser
    hits = pygame.sprite.groupcollide(meteor_list, bullets, True, True)
    for hit in hits:
        score += 10
        #explosion_sound.play()
        explosion = Explosion(hit.rect.center)
        all_sprites.add(explosion)
        meteor = Meteor()
        all_sprites.add(meteor)
        meteor_list.add(meteor)

    # Checar colisiones - jugador - meteoro
    hits = pygame.sprite.spritecollide(player, meteor_list, True)
    for hit in hits:
        player.shield -= 25
        meteor = Meteor()
        all_sprites.add(meteor)
        meteor_list.add(meteor)
        if player.shield <= 0:
            game_over = True
            show_game_over_screen()

    screen.blit(background, [0, 0])

    all_sprites.draw(screen)

    # MARCADOR
    draw_text(screen, str(score), 25, WIDTH // 2, 10)

    # BARRA DE VIDA
    draw_shield_bar(screen, 5, 5, player.shield)

    pygame.display.flip()

pygame.quit()










'''









def draw_text_with_border(surface, text, size, x, y, color, border_color):
	font = pygame.font.Font(None, size)
	text_surface = font.render(text, True, color)
	text_rect = text_surface.get_rect(center=(x, y))
	border_rect = pygame.Rect(text_rect.left - 2, text_rect.top - 2, text_rect.width + 4, text_rect.height + 4)
	pygame.draw.rect(surface, border_color, border_rect)
	surface.blit(text_surface, text_rect)

def show_go_screen():
	screen.blit(background, [0,0])
	draw_text_with_border(screen, "SHOOTER 2", 110, WIDTH // 2, HEIGHT // 4, (255, 255, 0), (0, 0, 0))
	draw_text_with_border(screen, "PUEDES HACER 1000 PUNTOS?", 50, WIDTH // 2, HEIGHT // 2, (255, 255, 0), (0, 0, 0))
	draw_text_with_border(screen, "ESTAS LISTO?", 40, WIDTH // 2, HEIGHT * 3/4, (255, 255, 0), (0, 0, 0))
	draw_text_with_border(screen, "PRESIONA UNA TECLA", 35, WIDTH // 2, HEIGHT * 3/4 + 60, (255, 255, 0), (0, 0, 0))
	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYUP:
				waiting = False

#PANTALLA DE JUEGO PERDIDO(GAME OVER)
def show_game_over_screen():
	screen.fill((0, 0, 0))
	draw_text_with_border(screen, "Perdiste fracasado", 40, WIDTH // 2, HEIGHT // 2, (255, 255, 0), (0, 0, 0))
	pygame.display.flip()
	pygame.time.wait(2000)


meteor_images = []
meteor_list = ["assets\meteorGrey_big1.png","assets\meteorGrey_big4.png","assets\meteorGrey_small1.png", "assets\meteorGrey_med1.png"]
for img in meteor_list:
	meteor_images.append(pygame.image.load(img).convert())



####----------------EXPLOSTION IMAGENES --------------

 
explosion_anim=[]
for i in range(0,2):
    file="assets/regularExplosion0{}.png".format(i) 
    img= pygame.image.load(file).convert()
    img.set_colorkey(BLACK)
    img_scale=pygame.transform.scale(img, (70,70))
    explosion_anim.append(img_scale) 

# CARGAR IMAGENES DE FONDO
background = pygame.image.load("assets/nebulosa-via-lactea.png").convert()

# CARGAR SONIDOS
laser_sound = pygame.mixer.Sound("assets/laser5.ogg")
explosion_sound = pygame.mixer.Sound("assets/explosion.ogg")
pygame.mixer.music.load("assets/boss.ogg")
pygame.mixer.music.set_volume(0.2)


pygame.mixer.music.play(loops=-1)


#### ----------GAME OVER
game_over = True
running = True
while running:
	if game_over:

		show_go_screen()
  

		game_over = False
		all_sprites = pygame.sprite.Group()
		meteor_list = pygame.sprite.Group()
		bullets = pygame.sprite.Group()

		player = Player()
		all_sprites.add(player)
		for i in range(8):
			meteor = Meteor()
			all_sprites.add(meteor)
			meteor_list.add(meteor)

		score = 0


	clock.tick(60)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				player.shoot()


	all_sprites.update()

	#colisiones - meteoro - laser
	hits = pygame.sprite.groupcollide(meteor_list, bullets, True, True)
	for hit in hits:
		score += 10
		#explosion_sound.play()
		explosion = Explosion(hit.rect.center)
		all_sprites.add(explosion)
		meteor = Meteor()
		all_sprites.add(meteor)
		meteor_list.add(meteor)

	# Checar colisiones - jugador - meteoro
	hits = pygame.sprite.spritecollide(player, meteor_list, True)
	for hit in hits:
		player.shield -= 25
		meteor = Meteor()
		all_sprites.add(meteor)
		meteor_list.add(meteor)
		if player.shield <= 0:
			game_over = True

	screen.blit(background, [0, 0])

	all_sprites.draw(screen)

	#MARCADOR
	draw_text(screen, str(score), 25, WIDTH // 2, 10)

	# BARRA DE VIDA
	draw_shield_bar(screen, 5, 5, player.shield)
 
 

	pygame.display.flip()
pygame.quit()
'''
