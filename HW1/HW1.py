from vpython import *

# environment
scene = canvas(width = 650, height = 480, align = 'left', center = vec(0,5,0), background = vec(0, 0.6, 0.6))
floor = box(length = 30, height = 0.01, width = 10, color = color.blue)

# scientific constants
g = 9.8 # g = 9.8 m/s^2
C_drag = 0.9 # drag coefficient = 0.9

# ball
size = 0.25 # ball radius = 0.25 m
theta = pi/4 # initial launch angle
ball = sphere(radius = size, color = color.red, make_trail = True)
ball.pos = vec(-15, size, 0) # initial position
ball.v = vec(20*cos(theta), 20*sin(theta), 0) # initial velocity

# ball arrow
barrow = arrow(color = color.cyan, shaftwidth = size/2)

# graph
vtgraph = graph(width = 600, height = 450, align = 'right', title = 'Speed-time diagram', xtitle = 'Time(s)', ytitle = 'Speed(m/s)', xmax = 4.5, ymax = 25)
vtcurve = gcurve(graph = vtgraph, color=color.blue, width=4)

# simulation

dt = 0.001 # time between steps
t = 0 # calculate time
distance = 0 # calculate distance travelled
count = 0 # count bounce times

while count < 3: # run until the ball hit the ground
    rate(1000) # loop rate
    t += dt
    
    # ball
    ball.v += (vec(0, -g, 0) - C_drag*ball.v) *dt # dv = a*dt
    ball.pos += ball.v*dt # dr = v*dt
    distance += mag(ball.v)*dt # ds = v(speed)*dt
    
    # ball arrow
    barrow.pos = ball.pos
    barrow.axis = ball.v/2 # proportion = 0.5
    
    # graph
    vtcurve.plot(pos=(t, mag(ball.v)))
    
    # check if ball hits the ground
    if ball.v.y < 0 and ball.pos.y <= size : 
        count += 1
        ball.v.y = - ball.v.y
    
    # largest height
    if abs(ball.v.y) <= 0.005 and count == 0 : # vy = 0 <=> largest height
        maxheight_pos = vec(ball.pos)

# after simulation
barrow.visible = False

rod1 = cylinder(pos = vec(maxheight_pos.x, size, 0), axis = vec(0, maxheight_pos.y - size, 0), radius = 0.07, color = color.cyan)
msg1 = text(text = f'Largest height = {maxheight_pos.y:.2f}', pos = vec(maxheight_pos.x, maxheight_pos.y + 1, 0), align = 'center', height = 0.8)

rod2 = cylinder(pos = vec(-15, size, 0), axis = vec(ball.pos.x-(-15), 0, 0), radius = 0.07, color = color.cyan)
msg2 = text(text = f'Displacement = {ball.pos.x-(-15):.2f}', pos = vec(2, 1.5, 0), height = 0.8)

msg3 = text(text = f'Distance = {distance:.2f}', pos = vec(2, 3, 0), height = 0.8)