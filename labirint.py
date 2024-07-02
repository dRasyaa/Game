from pygame import*

warna_background = (119,210,223)
mw = display.set_mode((800,650))


#hallo ini kak Dana
mw.fill(warna_background)
class karakter(sprite.Sprite):
    def __init__(self, x, y, panjang, lebar, nama):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(nama),(panjang, lebar))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def gambar(self):
        mw.blit(self.image,(self.rect.x, self.rect.y))
class mc(karakter):
    def __init__(self, x, y, panjang, lebar, nama, speed_x, speed_y):
        super().__init__(x, y, panjang, lebar, nama)
        self.speed_x = speed_x
        self.speed_y = speed_y
    def update(self):
        x_old = self.rect.x
        y_old = self.rect.y
        if player.rect.x > 0 and player.speed_x <0 or player.speed_x >0 and player.rect.x <730:
           self.rect.x += self.speed_x
        tabrak_tembok = sprite.spritecollide(self, wall, False)
        if self.speed_x >0:
            for i in tabrak_tembok:
                self.rect.right = min(self.rect.right, i.rect.left)
        elif self.speed_x <0:
            for i in tabrak_tembok:
                self.rect.left = max(self.rect.left, i.rect.right)
        if player.rect.y > 0 and player.speed_y <0 or player.speed_y >0 and player.rect.y <580:
           self.rect.y += self.speed_y
        tabrak_tembok = sprite.spritecollide(self, wall, False)
        if self.speed_y <0:
            for i in tabrak_tembok:
                self.rect.top = max(self.rect.top, i.rect.bottom)
        elif self.speed_y >0:
            for i in tabrak_tembok:
                self.rect.bottom = min(self.rect.bottom, i.rect.top)
    def shoot(self):
        bullet = peluru(self.rect.x, self.rect.y, 20,10, 'bullet.png', 15)
        bullets.add(bullet)
class enemy(karakter):
    def __init__(self, x, y, panjang, lebar, nama, speed):
        super().__init__(x, y, panjang, lebar, nama)
        self.speed = speed
        self.move = 'left'
    def update(self):
        if self.rect.x >= 700:
            self.move = 'left'
        if self.rect.x <= 400:
            self.move = 'right'
        if self.move == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
class peluru(karakter):
    def __init__(self, x, y, panjang, lebar, nama, speed):
        super().__init__(x, y, panjang, lebar, nama)
        self.speed = speed
    def update(self):
        self.rect.x += self.speed
        if self.rect.x >= 800:
            self.kill()

player = mc(50, 600, 70,70, 'game.png', 0, 0)
musuh = enemy(550, 500, 70, 70, 'ghost.png',3)
tembok = karakter(300, 80, 100, 600, 'wall.png')
finish = karakter(620, 570, 60, 60, 'flag.png')
wall = sprite.Group()
wall.add(tembok)
bullets = sprite.Group()
hantu = sprite.Group()
hantu.add(musuh)

run = True
while run:
    mw.fill(warna_background )
    player.gambar()
    player.update()
    hantu.draw(mw)
    hantu.update()
    wall.draw(mw)
    finish.gambar() 
    
    if sprite.spritecollide(player, hantu, False):
        game_over = image.load('game_over.jpg')
        mw.fill((45,65,70))
        mw.blit(transform.scale(game_over, (800,650)), (0,0))
    if sprite.collide_rect(player, finish):
        menang = image.load('win.jpg')
        mw.fill((45,45,54))
        mw.blit(transform.scale(menang, (800,650)), (0,0))
    sprite.groupcollide(hantu, bullets, True, True)
    sprite.groupcollide(wall, bullets, False, True)
    for i in event.get():
        if i.type == QUIT:
            run = False
        if i.type == KEYDOWN:
            if i.key == K_d:
                player.speed_x = 5
            if i.key == K_a:
                player.speed_x = -5
            if i.key == K_w:
                player.speed_y = -5
            if i.key == K_s:
                player.speed_y = 5
            if i.key == K_j:
                player.shoot()
        if i.type == KEYUP:
            if i.key == K_d:
                player.speed_x = 0
            if i.key == K_a:
                player.speed_x = 0
            if i.key == K_w:
                player.speed_y = 0
            if i.key == K_s:
                player.speed_y = 0

    bullets.update()
    bullets.draw(mw)
    display.update()
    time.delay(40)
