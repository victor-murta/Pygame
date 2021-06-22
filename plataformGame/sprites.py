#classes dos sprites
from settings import *
import pygame as pg

from random import choice, randrange
vec = pg.math.Vector2

class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # image = pg.transform.scale(image, (width // 2, height // 2))
        image = pg.transform.scale(image, (70, 70))
        return image
            
class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = player_layer
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (40, height - 100)
        self.pos = vec(40, height - 100)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)


    def load_images(self):
        self.standing_frames = [
            self.game.spritesheet.get_image(1, 1, 202, 150),
            self.game.spritesheet.get_image(205, 1, 202, 151),
            self.game.spritesheet.get_image(409, 1, 201, 150),

        ]

        for frame in self.standing_frames:
            frame.set_colorkey(white)
        
        self.walk_frames_r = [
            self.game.spritesheet.get_image(1, 1, 202, 150),
            self.game.spritesheet.get_image(205, 1, 202, 151),
        ]

        self.walk_frames_l = []

        for frame in self.walk_frames_r:
            frame.set_colorkey(white)
            #Horizontal ,vertical
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))
        
        


    def jump(self):
        #pular somente se estiver em uma plataforma
        self.rect.x += 2
        hits = pg.sprite.spritecollide(self, self.game.plataforms, False)
        self.rect.x -= 2
        if hits :
            self.game.jump_sound.play()
            self.jumping = True
            self.vel.y = -player_jump


    def update(self):
        self.animate()

        self.acc = vec(0 , player_grav)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -player_acc
        if keys[pg.K_RIGHT]:
            self.acc.x = player_acc

        
        #fricções
        self.acc.x += self.vel.x * player_friction
        # equações de movimentação
        self.vel += self.acc

        if abs(self.vel.x) < 0.2:
            self.vel.x = 0

        self.pos += self.vel + 0.5 * self.acc
        # transitar pelos lados da tela
        if self.pos.x > width + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2

        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = width + self.rect.width / 2

        self.rect.midbottom = self.pos

                
    def animate(self):
        now = pg.time.get_ticks()

        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking =False

        if self.walking:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom

                if self.vel.x > 0:
                    self.image = self.walk_frames_l[self.current_frame]
                else:
                    self.image = self.walk_frames_r[self.current_frame]

                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

class Plataform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = plataform_layer
        self.groups = game.all_sprites, game.plataforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        images = [self.game.spritesheet.get_image(612, 1, 381, 95),
                  self.game.spritesheet.get_image(995, 1, 202, 102)]
        self.image = choice(images)
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        if randrange(100) < pow_spaw_pct:
            Pow(self.game, self)

class Pow(pg.sprite.Sprite):
    def __init__(self, game, plat):
        self._layer = pow_layer
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = choice(['boost'])
        self.image = self.game.spritesheet.get_image(1505, 1, 95, 98)
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5

    
    def update(self):
        self.rect.bottom = self.plat.rect.top - 5

        if not self.game.plataforms.has(self.plat):
            self.kill()


class Mob(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = mob_layer
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image_up = self.game.spritesheet.get_image(1352, 1, 67, 94)
        self.image_up.set_colorkey(black)
        self.image_down = self.game.spritesheet.get_image(1288, 1, 62, 94)
        self.image_down.set_colorkey(black)
        self.image = self.image_up
        self.rect = self.image.get_rect()
        self.rect.centerx = choice([-100, width + 100])
        self.vx = randrange(1, 4)
        if self.rect.centerx > width:
            self.vx *= -1
        self.rect.y = randrange(height / 2)
        self.vy = 0
        self.dy = 0.5

    def update(self):
        self.rect.x += self.vx
        self.vy += self.dy
        if self.vy > 3 or self.vy < -3:
            self.dy *= -1
        center = self.rect.center
        if self.dy < 0:
            self.image = self.image_up
        else:
            self.image = self.image_down
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.rect.y += self.vy
        if self.rect.left > width + 100 or self.rect.right < -100:
            self.kill()
    