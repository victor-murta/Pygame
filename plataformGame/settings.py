width = 480
height = 600
fps = 60
title = "Por água acima"
font_name = 'Terminal'
hs_file = 'hightscore.txt'
SPRITESHEET = "sprites.png"

#propriedades do jogador
player_acc = 0.5
player_friction = -0.12
player_grav = 0.8
player_jump = 20

#plataformas
plataform_list = [(0,height - 40, width, 40),
    (width / 2 - 50, height * 3 / 4 ,100, 20 ),
    (125, height - 350, 100, 20),
    (350, 200, 100, 20),
    (175, 100, 50, 20),
    (22, 100, 50, 20)
]

#plataformas
plataform_positions = [(width, 40),
    (100, 20 ),
    (100, 20),
    (100, 20),
    (50, 20),
    (50, 20)
]

#cores
white = (255, 255, 255)
black = (0,0,0)
green = (0, 255, 0)
blue  = (0,0,255)
light_blue = (0,155, 155)
bgcolor = black




