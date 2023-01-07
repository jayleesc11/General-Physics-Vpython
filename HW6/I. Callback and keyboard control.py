from vpython import *
pos, angle = vec(0, 0, 0), 0

def keyinput(evt): #keyboard callback function
    global pos, angle
    move = {'left': vec(-0.1, 0, 0), 'right': vec(0.1, 0, 0),
    'up': vec(0, 0.1, 0),
    'down': vec(0, -0.1, 0), 'i' : vec(0, 0, -0.1),
    'o': vec(0, 0, 0.1)}
    roa = {'c' : pi / 90.0 , 'r': - pi / 90.0}
    s = evt.key
    if s in move : pos += move[s]
    if s in roa:
        ball.rotate(angle = roa[s], axis = vec(0, 0, 1), origin= ball.pos)
        angle -= roa[s]

scene = canvas(width=800, height=800, range = 5, background=color.white)
ball = sphere(radius = 2.0, texture=textures.earth )
scene.bind('keydown', keyinput) # setting for the binding function

while True:
    rate(1000)
    ball.rotate(angle=pi/600, axis= vec(sin(angle),cos(angle),0),
    origin=pos)
    ball.pos = pos