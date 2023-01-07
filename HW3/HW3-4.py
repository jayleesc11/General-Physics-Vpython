from vpython import*

# Environment
scene = canvas(width = 540, height = 500, align = 'left')

# Constants
mass = {'earth': 5.97E24, 'moon': 7.36E22, 'sun':1.99E30}
radius = {'earth': 6.371E6*10, 'moon': 1.317E6*10, 'sun': 6.95E8*10} #10 times larger for better view
earth_orbit = {'r': 1.495E11, 'v': 2.9783E4}
moon_orbit = {'r': 3.84E8, 'v': 1.022E3}
theta = 5.145 * pi / 180.0

# Objects
## Earth
earth = sphere(radius = radius['earth'], m = mass['earth'], texture = textures.earth)
earth.pos = vec(0, 0, 0)
earth.v = vec(0, 0, 0)

## Moon
moon = sphere(radius = radius['moon'], m = mass['moon'], make_trail = True)
moon.v = vec(0, 0, -moon_orbit['v'])
moon.pos = vec(moon_orbit['r'] * cos(theta), -moon_orbit['r'] * sin(theta), 0)

## EM_COM
def COM_vec(m1, m2, vec1, vec2):
    return (vec1 * m1 + vec2 * m2) / (m1 + m2)

COM_pos_shift = COM_vec(earth.m, moon.m, earth.pos, moon.pos)
COM_v_shift = COM_vec(earth.m, moon.m, earth.v, moon.v)

earth.pos -= COM_pos_shift
earth.v -= COM_v_shift

moon.pos -= COM_pos_shift
moon.v -= COM_v_shift

# Objects modification: add sun
sun = sphere(radius = radius['sun'], m = mass['sun'], color = color.orange, emissive=True)
earth.pos += vec(earth_orbit['r'], 0, 0)
moon.pos += vec(earth_orbit['r'], 0, 0)
earth.v += vec(0, 0, -earth_orbit['v'])
moon.v += vec(0, 0, -earth_orbit['v'])

# Gravitational force m2 exert to m1
G = 6.673E-11
def G_force(m1, m2, pos1, pos2):
    return -G * m1 * m2 / mag2(pos1 - pos2) * norm(pos1 - pos2)

# Simulation
dt = 60 * 6

while(True):
    rate(1000)

    moon.a = G_force(moon.m, earth.m, moon.pos, earth.pos) / moon.m
    earth.a = G_force(earth.m, moon.m, earth.pos, moon.pos) / earth.m

    ## Modification 
    moon.a += G_force(moon.m, sun.m, moon.pos, sun.pos) / moon.m
    earth.a += G_force(earth.m, sun.m, earth.pos, sun.pos) / earth.m

    moon.v += moon.a * dt
    moon.pos += moon.v * dt
    earth.v += earth.a * dt
    earth.pos += earth.v * dt
    scene.center = earth.pos