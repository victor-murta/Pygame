'''
Integrantes do grupo:
    - Marco Couto
    - Caio Moura
    - Caio Rangel
    - Leandro Moreira
    - Victor Murta
'''

#Arquivos I/O : input/output

import pygame as pg
import random
from settings import *
from sprites import *
from os import path

class Game:
    def __init__(self):
        #iniciando a janela do jogo
        # começar o jovo novamente
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((width, height))
        pg.display.set_caption(title)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(font_name)
        self.load_data()

    def load_data(self):
        #carregando maior pontuação / carregando os personagens do jogo
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img2')
        with open(path.join(self.dir, hs_file), 'r') as f:
            try:
                self.hightscore = int(f.read())
            except:
                self.hightscore = 0

        #Carregando os sprites
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))

        #Carregando sons
        self.snd_dir = path.join(self.dir, 'snd')
        self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir, 'jumpingSound.wav'))
        self.boost_sound = pg.mixer.Sound(path.join(self.snd_dir, 'boost.wav'))



    def new(self):
        #loop do game // criando uma janela
        self.score = 0
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.plataforms = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.powerups= pg.sprite.Group()
        self.player = Player(self)
        for plat in plataform_list:
            Plataform(self, *plat)
        self.mob_timer = 0
        pg.mixer.music.load(path.join(self.snd_dir, 'snd.mpeg'))
        self.run()

    def run(self):
        #loop do jogo 
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(fps)
            self.events()
            self.update()
            self.draw() 
        pg.mixer.music.fadeout(500)
    
    def update(self):
        #atualização do jogo - update
        self.all_sprites.update()

        # inserindo inimigo
        now = pg.time.get_ticks()
        if now - self.mob_timer > 5000 + random.choice([-1000,-500, 0, 500, 1000]):
            self.mob_timer = now
            Mob(self)

        mob_hits = pg.sprite.spritecollide(self.player, self.mobs, False)
        if mob_hits:
            self.playing = False


        #checar se o jogador fica por cima da plataforma se ele pular sobre
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.plataforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.x < lowest.rect.right + 10 and \
                    self.player.pos.x > lowest.rect.left - 10:

                    if self.player.pos.y < lowest.rect.centery:
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0  
                        self.player.jumping = False

        # jogador tocar na parte de cima da tela
        if self.player.rect.top <= height / 4:
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for mob in self.mobs:
                mob.rect.y += max(abs(self.player.vel.y), 2)  

            for plat in self.plataforms:
                plat.rect.y += max(abs(self.player.vel.y), 2)  
                if plat.rect.top >= height:
                    plat.kill()
                    #a cada plataforma , mais 10 pontos
                    self.score += 10

        
        # encostando no poder
        pow_hits = pg.sprite.spritecollide(self.player, self.powerups, True)
        for pow in pow_hits:
            if pow.type == 'boost':
                
                self.boost_sound.play()
                self.player.vel.y = -boost_power
                self.player.jumping = False

        
        # Morrendo
        if self.player.rect.bottom > height: 
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.plataforms) == 0:
            self.playing = False

        # novas plataformas
        while len(self.plataforms) < 6:
            WIDTH = random.randrange(50, 100)
            Plataform(self, random.randrange(0, width - WIDTH),
                random.randrange(-75, -30))

    def events(self):
        # loop do jog - eventos
        for event in pg.event.get():
            #fechando a aba
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False

                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
                            

    def draw(self):
        # desenhando os eventos
        self.screen.fill(bgcolor)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 42 , white, width / 2, 20)

        # depois de desenhar tudo, troque o display
        pg.display.flip()

    def show_start_screen(self):
        # inicio do jogo
        pg.mixer.music.load(path.join(self.snd_dir, 'Yippee.ogg'))
        pg.mixer.music.play(loops=-1)
        self.screen.fill(bgcolor)
        self.draw_text(title, 48 , white, width / 2, height / 4)
        self.draw_text("Setas para se movimentar e espaço para pular", 22, white, width / 2, height / 2)
        self.draw_text("Aperte qualquer tecla para começar", 22, white, width / 2, height *3 / 4)
        self.draw_text("Maior pontuação: "+ str(self.hightscore), 32, white, width / 2, 15)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)


    def show_go_screen(self):
        # perdeu (game over) / continuar
        if not self.running:
            return 
        pg.mixer.music.load(path.join(self.snd_dir, 'deadMusic.mp3'))
        pg.mixer.music.play()
        self.screen.fill(bgcolor)
        self.draw_text("FIM DE JOGO", 48 , white, width / 2, height / 4)
        self.draw_text("Score: "+str(self.score), 35, white, width / 2, height / 2)
        self.draw_text("Aperte qualquer tecla para jogar novamente", 22, white, width / 2, height *3 / 4)
        if self.score > self.hightscore:
            self.hightscore = self.score
            self.draw_text('Maior pontuação conquistada!', 32, white, width /2, height / 2 + 40 )
            with open(path.join(self.dir, hs_file), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text('Maior pontuação: '+ str(self.hightscore), 32, white, width / 2, height / 2 + 40)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)


    #função que aguarda o jogador apertar uma tecla no inicio do jogo
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(fps)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running  = False

                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()

