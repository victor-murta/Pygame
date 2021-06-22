width = 480
height = 600
fps = 60
title = "Por água acima"
font_name = 'Terminal'
hs_file = 'hightscore.txt'
SPRITESHEET = "spritesheet.png"

#propriedades do jogador
player_acc = 0.5
player_friction = -0.12
player_grav = 0.8
player_jump = 20

# propriedades do jogo
boost_power = 60  # distância
pow_spaw_pct = 7  #de 7 em 7 plataforma terá um poder(queijo)
mob_fre = 5000 # 5 segundos
player_layer = 2
plataform_layer = 1
pow_layer = 1
mob_layer = 2

#plataformas
plataform_list = [
    (0, height - 60),
    (width / 2 - 50, height * 3 / 4 - 50),
    (125, height - 350),
    (350, 200),
    (175, 100)
]

#cores
white = (255, 255, 255)
black = (0,0,0)
green = (0, 255, 0)
blue  = (0,0,255)
light_blue = (0,155, 155)
bgcolor = light_blue




