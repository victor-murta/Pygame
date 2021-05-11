#classes dos sprites
from settings import *
import pygame as pg
import json
from random import choice
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
        pg.sprite.Sprite.__init__(self)
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
            self.game.spritesheet.get_image(95, 34, 33, 34),
            self.game.spritesheet.get_image(0, 119, 31, 29)
        ]

        for frame in self.standing_frames:
            frame.set_colorkey(white)
        
        self.walk_frames_r = [
            self.game.spritesheet.get_image(0, 148, 31, 27),
            self.game.spritesheet.get_image(0, 119, 31, 29)
        ]

        self.walk_frames_l = []

        for frame in self.walk_frames_r:
            frame.set_colorkey(white)
            #Horizontal ,vertical
            self.walk_frames_l.append(pg.transform.flip(frame, False, True))
        
        


    def jump(self):
        #pular somente se estiver em uma plataforma
        self.rect.x += 2
        hits = pg.sprite.spritecollide(self, self.game.plataforms, False)
        self.rect.x -= 2
        if hits:
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
                    self.image = self.walk_frames_r[self.current_frame]
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
        pg.sprite.Sprite.__init__(self)
        self.game = game
        images = [
            self.game.spritesheet.get_image(32, 94, 32, 24),
            self.game.spritesheet.get_image(48, 35, 33, 27)
        ]
        self.image = choice(images)
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y