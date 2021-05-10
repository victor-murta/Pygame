#classes dos sprites
from settings import *
import pygame as pg
import json
import random
vec = pg.math.Vector2

class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.filename = filename
        self.spritesheet = pg.image.load(filename).convert()
        self.meta_data = self.filename.replace('png', 'json')
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.set_colorkey((255,255,255))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        return image

    def parse_sprite(self, name):
        sprite = self.data['frames'][name]['frame']
        x, y, w, h = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        image = self.get_image(x, y, w, h)
        return image

        
class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        # self.load_images()
        self.image = self.game.spritesheet.parse_sprite('rato1.png')
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height / 2)
        self.pos = vec(width / 2, height / 2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    # def load_images(self):
    #     self.standing_frames = []

    def update(self):
        # self.animate()
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
        self.pos += self.vel + 0.5 * self.acc
        # transitar pelos lados da tela
        if self.pos.x > width:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = width

        self.rect.midbottom = self.pos

                
    
    def jump(self):
        #pular somente se estiver em uma plataforma
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.plataforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -player_jump


class Plataform(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = self.game.spritesheet.parse_sprite('plataforma1.png')
        if bool(random.getrandbits(1)):
            self.image = self.game.spritesheet.parse_sprite('plataforma2.png')

        self.image = self.image.convert()
        self.image = pg.transform.scale(self.image, (w, h))
        self.image.set_colorkey(white)


        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y