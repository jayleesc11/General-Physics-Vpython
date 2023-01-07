from vpython import *

# environment
scene = canvas(width=500, height=500, center=vec(0, -0.2, 0), background=vec(0.5,0.5,0))
ceiling = box(length=0.8, height=0.005, width=0.8, color=color.blue)

#constant
g = 9.8  # g = 9.8 m/s^2
size, m = 0.02, 0.5 # ball radius and mass
L, k = 0.5, 15000 # spring force constant and length

# ball
ball = sphere(radius = size, color=color.red)
ball.v = vec(0.6, 0, 0)
ball.pos = vec(0, -L - m*g/k, 0)

# rope: a spring with large k
spring = cylinder(radius=0.005) # default pos = vec(0, 0, 0)

# stimulation
dt = 0.001
while True:
    rate(1000)
    spring.axis = ball.pos - spring.pos
    spring_force = - k * (mag(spring.axis) - L) * spring.axis.norm()
    ball.a = vector(0, - g, 0) + spring_force / m # ball acceleration = - g in y + spring force /m
    
    ball.v += ball.a*dt
    ball.pos += ball.v*dt