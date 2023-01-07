from vpython import *

# Environment
scene = canvas(width = 540, height = 500, align = 'left', center = vec(0.8, -1, 0.6), background = vec(0, 0.6, 0.6))

# Constants
N = int(input("How many balls do you want to lift (1~4)?  ")) # ask user to input number of lifted balls
g = vec(0, -9.8, 0)     # gravitational acceleration
size, m = 0.2, 1        # balls radius and mass
k = 150000              # rope force constant
L = 2 - m*mag(g)/k      # rope original length
d = 0.4                 # distance betwwen pivots

# Each pendulum setting
pivots = []
ropes = []
balls = []

for i in range(5):
    # Pivots
    pivot = sphere(pos = vec(d*i, 0, 0), radius = 0.04, color=color.blue)
    pivots.append(pivot) # add new pivot to the "pivots" list
    
    # Ropes
    rope = cylinder(pos = pivots[i].pos, axis = vec(0, - L - m*mag(g)/k, 0), radius = 0.01, color=color.blue)
    ropes.append(rope) # add new rope to the "ropes" list

    # Balls
    ball = sphere(pos = pivots[i].pos + ropes[i].axis, radius = size, color=color.red)
    ball.v = vec(0, 0, 0)
    balls.append(ball) # add new ball to the "balls" list

# Lifted ball setting
for i in range(N):
    balls[i].pos += vec(-sqrt(L**2 - 1.95**2), + m*mag(g)/k + L - 1.95, 0)
    
# Function: after collision velocity
def af_col_v(m1, m2, v1, v2, x1, x2):
    v1_prime = v1 + 2*(m2/(m1+m2))*(x1-x2) * dot (v2-v1, x1-x2) / dot (x1-x2, x1-x2)
    v2_prime = v2 + 2*(m1/(m1+m2))*(x2-x1) * dot (v1-v2, x2-x1) / dot (x2-x1, x2-x1)
    return (v1_prime, v2_prime)

# Graph1
instant_graph = graph(width = 700, height = 225, align = 'right', title = 'K & U-time diagram', xtitle = 'Time(s)', ytitle = 'K & U (J)')
instant_K = gcurve(graph = instant_graph, color = color.blue, width = 2, label = "K")
instant_U = gcurve(graph = instant_graph, color = color.red, width = 2, label = "U")

# Graph2
average_graph = graph(width = 700, height = 225, align = 'right', title = 'Average K & U-time diagram', xtitle = 'Time(s)', ytitle = 'K & U (J)')
average_K = gcurve(graph = average_graph, color = color.blue, width = 2, label = "K")
average_U = gcurve(graph = average_graph, color = color.red, width = 2, label = "U")

# Simulation
dt = 0.0001
t = 0
K_t_integral = 0 
U_t_integral = 0

while True:
    rate(5000) # loop rate
    t += dt
    K = 0
    U = 0
    
    for i in range(5):
    
        # Ropes
        ropes[i].axis = balls[i].pos - ropes[i].pos
        ropes[i].force = - k * (mag(ropes[i].axis) - L) * ropes[i].axis.norm()
        
        # Balls
        balls[i].a = g + ropes[i].force / m
        balls[i].v += balls[i].a * dt
        balls[i].pos += balls[i].v * dt
        
        # Energy
        K += 1/2 * m * mag(balls[i].v)**2 # sum the instant kinetic energy of each ball
        U += m * mag(g) * (balls[i].pos.y - (-L - m*mag(g)/k)) # sum the instant potential energy of each ball
      
    # Graph1
    instant_K.plot(pos = (t, K))
    instant_U.plot(pos = (t, U))
    
    # Graph2
    K_t_integral += K * dt
    U_t_integral += U * dt
    average_K.plot(pos = (t, K_t_integral / t))
    average_U.plot(pos = (t, U_t_integral / t))
    
    # Collisions
    for i in range(4):
        if (mag(balls[i].pos - balls[i+1].pos) <= 2*size and dot(balls[i].pos-balls[i+1].pos, balls[i].v-balls[i+1].v) <= 0) : # contact and approaching
            (balls[i].v, balls[i+1].v) = af_col_v (m, m, balls[i].v, balls[i+1].v, balls[i].pos, balls[i+1].pos) # count after collision velocity      