#classes dos sprites
from settings import *
import pygame as pg
import json
import random
from os import path
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
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # image = pg.transform.scale(image, (width // 2, height // 2))
        image = pg.transform.scale(image, (70, 70))
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
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (40, height - 100)
        self.pos = vec(40, height - 100)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.dir = path.dirname(__file__)
        self.sound_dir = path.join(self.dir, 'sound')


    def load_images(self):
        self.standing_frames = [
            self.game.spritesheet.parse_sprite('rato1.png'),
            self.game.spritesheet.parse_sprite('rato2.png'),
            self.game.spritesheet.parse_sprite('rato3.png'),
            self.game.spritesheet.parse_sprite('rato4.png'),
            self.game.spritesheet.parse_sprite('rato5.png'),
            self.game.spritesheet.parse_sprite('rato6.png'),
            self.game.spritesheet.parse_sprite('rato7.png')
        ]

        for frame in self.standing_frames:
            frame.set_colorkey(white)
        
        self.walk_frames_r = [
            self.game.spritesheet.parse_sprite('RatoAndandoEsquerda.png'),
            self.game.spritesheet.parse_sprite('RatoAndandoEsquerdaParado.png')
        ]

        for frame in self.walk_frames_r:
            frame.set_colorkey(white)
            #Horizontal ,vertical
            # self.walk_frames_l.append(pg.transform.flip(frame, False, True))

        self.walk_frames_l = [
            self.game.spritesheet.parse_sprite('RatoAndandoDireita.png'),
            self.game.spritesheet.parse_sprite('RatoAndandoDireitaParado.png')
        ]

        for frame in self.walk_frames_l:
            frame.set_colorkey(white)
            #Horizontal ,vertical
            # self.walk_frames_l.append(pg.transform.flip(frame, False, True))
        


    def jump(self):
        #pular somente se estiver em uma plataforma
        self.rect.x += 2
        hits = pg.sprite.spritecollide(self, self.game.plataforms, False)
        self.rect.x -= 2
        if hits:
            self.vel.y = -player_jump
            pg.mixer.music.load(path.join(self.sound_dir, 'rat-jump.wav'))
            pg.mixer.music.play(0)


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
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_r)
                bottom = self.rect.bottom

                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]

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
            self.game.spritesheet.parse_sprite('plataforma1.png'),
            self.game.spritesheet.parse_sprite('plataforma2.png')
        ]
        self.image = random.choice(images)
        self.image.set_colorkey(white)
        ratio = 1.77
        height_updated = random.randint(35, 70)
        width_updated = height_updated * ratio
        self.image = pg.transform.scale(self.image, (int(round(width_updated)), height_updated))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y