from vpython import*

# Environment
scene = canvas(width = 600, height = 500, align = 'left')
scene.light = []
local_light(pos = vec(0, 0, 0))

# Constants
mass = {'earth': 5.97E24, 'moon': 7.36E22, 'sun':1.99E30}
radius = {'earth': 6.371E6*10, 'moon': 1.317E6*10, 'sun': 6.95E8*10} #10 times larger for better view
earth_orbit = {'r': 1.495E11, 'v': 2.9783E4}
moon_orbit = {'r': 3.84E8, 'v': 1.022E3}
theta = 5.145 * pi / 180.0

# Objects
## Sun
sun = sphere(radius = radius['sun'], m = mass['sun'], color = color.orange, emissive = True)

## Earth
earth = sphere(radius = radius['earth'], m = mass['earth'], texture = textures.earth)
earth.pos = vec(0, 0, 0)
earth.v = vec(0, 0, 0)

## Moon
moon = sphere(radius = radius['moon'], m = mass['moon'])
moon.pos = vec(moon_orbit['r'] * cos(theta), -moon_orbit['r'] * sin(theta), 0)
moon.v = vec(0, 0, -moon_orbit['v'])

## EM_COM
def COM_vec(m1, m2, vec1, vec2):
    return (vec1 * m1 + vec2 * m2) / (m1 + m2)

COM_pos_shift = COM_vec(earth.m, moon.m, earth.pos, moon.pos)
COM_v_shift = COM_vec(earth.m, moon.m, earth.v, moon.v)

earth.pos -= COM_pos_shift
earth.v -= COM_v_shift

moon.pos -= COM_pos_shift
moon.v -= COM_v_shift

## Add sun
earth.pos += vec(earth_orbit['r'], 0, 0)
moon.pos += vec(earth_orbit['r'], 0, 0)
earth.v += vec(0, 0, -earth_orbit['v'])
moon.v += vec(0, 0, -earth_orbit['v'])

## Ecliptic normal arrow
arrown = arrow(color = color.yellow, shaftwidth = 5E6)

## Angle-time graph
angle_graph = graph(width = 650, height = 500, align = 'right', title = 'Angle-Time Graph', xtitle = 'Time (year)', ytitle = 'Angle (degree)')
angle_curve = gcurve(graph = angle_graph, color = color.blue)

# Gravitational force m2 exert to m1
G = 6.673E-11
def G_acc(m2, pos1, pos2):
    return -G * m2 / mag2(pos1 - pos2) * norm(pos1 - pos2)

# Simulation
t = 0
dt = 60 * 60
show = False
scene.camera.follow(earth)

while(True):
    rate(10000)
    t += dt/(365 * 86400)
    
    ## Moon
    moon.a = (G_acc(earth.m, moon.pos, earth.pos) + G_acc(sun.m, moon.pos, sun.pos))
    moon.v += moon.a * dt
    moon.pos += moon.v * dt

    ## Earth
    earth.a = (G_acc(moon.m, earth.pos, moon.pos) + G_acc(sun.m, earth.pos, sun.pos))
    earth.v += earth.a * dt
    earth.pos += earth.v * dt

    ## Ecliptic normal arrow
    arrown.pos = earth.pos
    arrown.axis = cross(moon.pos - earth.pos, moon.v - earth.v) * 0.00025

    ## Angle-time graph
    angle = (diff_angle(vec(1, 0, 0), arrown.axis) * 180/pi) - 90
    angle_curve.plot(pos = (t, angle))

    ## Show precession period
    if show == False and abs(angle) <= 0.001:
        print ("Precession period: ", 4*t, "years")
        show = True