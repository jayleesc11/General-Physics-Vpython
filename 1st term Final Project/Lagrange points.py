from vpython import *
ratio = 30
G = 6.67E-11
d_e_s = 149598023E3
m_sun = 1.98892E30
m_earth = 1.98892E30 / ratio
x_sun = vec(0, 0, 0)
x_earth = vec(d_e_s, 0, 0)
r_sun = 695700E3
r_earth = 6371E3
x_c = (m_sun * x_sun + m_earth * x_earth) / (m_sun + m_earth)

scene = canvas(width=1000, height=800)
earth = sphere(pos = x_earth, radius = r_earth)
sun = sphere(pos = x_sun, radius = r_sun)
omega = vec(0, 0, sqrt(G * (m_sun + m_earth) / (mag(x_earth - x_sun) ** 3)))

def force(x, v):
    if x == vec(0, 0, 0):
        return x, x, x, x
    try:
        f_e = G * m_earth / mag2(x-x_earth) * (x_earth-x).norm()
    except ZeroDivisionError:
        f_e = vec(0, 0, 0)
    try:
        f_s = G * m_sun / mag2(x-x_sun) * (x_sun-x).norm()
    except ZeroDivisionError:
        f_s = vec(0, 0, 0)
    f_ce = mag2(omega) * mag(x-x_c) * (x - x_c).norm()
    f_co = -2 * cross(omega, v)
    return f_e, f_s, f_ce, f_co

def total(*args):
    s = vec(0, 0, 0)
    for arg in args[0]:
        s = s + arg
    return s

k = 10

balls1 = [sphere(pos = vec(d_e_s * i / k, 0, 0), v = vec(0, 0, 0), radius = 1, color = color.red, make_trail = True, trail_radius = d_e_s / 10 * 0.01) for i in range(-int(k * 1.5), int(k * 1.5))]
balls2 = [sphere(pos = vec(d_e_s * i / k, 0, 0), v = vec(0, 0, 0), radius = 1, color = color.red, make_trail = True, trail_radius = d_e_s / 10 * 0.01) for i in range(-int(k * 1.5), int(k * 1.5))]
balls3 = [sphere(pos = vec(d_e_s * abs(i) / k * cos(pi/3), d_e_s * i / k * sin(pi/3), 0), radius = 1, color = color.red, make_trail = True, trail_radius = d_e_s / 10 * 0.01) for i in range(-int(k * 1.5), int(k * 1.5))]
balls4 = [sphere(pos = vec(d_e_s * abs(i) / k * cos(pi/3), d_e_s * i / k * sin(pi/3), 0), radius = 1, color = color.red, make_trail = True, trail_radius = d_e_s / 10 * 0.01) for i in range(-int(k * 1.5), int(k * 1.5))]

balls = []
arrs = []
balls.append(sphere(pos = vec(0, 0, 0), v = vec(0, 0, 0), radius = 1, color = color.black, make_trail = False, trail_radius = 1))
arrs.append([arrow(pos = vec(0, 0, 0), color = color.black, shaftwidth = 1E9), arrow(pos = vec(0, 0, 0), color = color.black, shaftwidth = 1E9), arrow(pos = vec(0, 0, 0), color = color.black, shaftwidth = 1E9), arrow(pos = vec(0, 0, 0), color = color.black, shaftwidth = 1E9)])
def draw(evt):
    c = vec(random(), random(), random())
    balls.append(sphere(pos = evt.pos, v = vec(0, 0, 0), radius = 1E9, color = c, make_trail = True, trail_radius = 5E8))
    arrs.append([arrow(pos = evt.pos, color = color.blue, shaftwidth = 1E9), arrow(pos = evt.pos, color = color.green, shaftwidth = 1E9), arrow(pos = evt.pos, color = color.red, shaftwidth = 1E9), arrow(pos = evt.pos, color = color.yellow, shaftwidth = 1E9)])
scene.bind("mousedown", draw)

t = 0
while True:
    t += 1
    if t > 7000: break
    for ball in balls1:
        ball.v = cross(total(force(ball.pos, vec(0, 0, 0))), vec(0, 0, 1)).norm()
        new_pos = ball.pos + ball.v * 5E7
        if ball.pos.y * new_pos.y < 0:
            ball.pos = vec(ball.pos.x + (new_pos.x - ball.pos.x) * ball.pos.y / (ball.pos.y - new_pos.y), 0, 0)
            ball.make_trail = False
        ball.pos = new_pos
    
    for ball in balls2:
        ball.v = -cross(total(force(ball.pos, vec(0, 0, 0))), vec(0, 0, 1)).norm()
        new_pos = ball.pos + ball.v * 5E7
        if ball.pos.y * new_pos.y < 0:
            ball.pos = vec(ball.pos.x + (new_pos.x - ball.pos.x) * ball.pos.y / (ball.pos.y - new_pos.y), 0, 0)
            ball.make_trail = False
        ball.pos = new_pos
    
    for ball in balls3:
        ball.v = cross(total(force(ball.pos, vec(0, 0, 0))), vec(0, 0, 1)).norm()
        new_pos = ball.pos + ball.v * 5E7
        if (new_pos.x - new_pos.y / sqrt(3)) * (ball.pos.x - ball.pos.y / sqrt(3)) < 0:
            try:
                ball.pos = vec(ball.pos.x + (new_pos.x - ball.pos.x) * ball.pos.y / (ball.pos.y - new_pos.y), 0, 0)
            except ZeroDivisionError:
                pass
            ball.make_trail = False
        ball.pos = new_pos
    
    for ball in balls4:
        ball.v = cross(total(force(ball.pos, vec(0, 0, 0))), vec(0, 0, 1)).norm()
        new_pos = ball.pos + ball.v * 5E7
        if (new_pos.x + new_pos.y / sqrt(3)) * (ball.pos.x + ball.pos.y / sqrt(3)) < 0:
            try:
                ball.pos = vec(ball.pos.x + (new_pos.x - ball.pos.x) * ball.pos.y / (ball.pos.y - new_pos.y), 0, 0)
            except ZeroDivisionError:
                pass            
            ball.make_trail = False
        ball.pos = new_pos
t = 0
dt = 1000
while True:
    if t > 250000: break
    for ball, arr in zip(balls, arrs):
        f = force(ball.pos, ball.v)
        ball.a = f[0] + f[1] + f[2] + f[3]
        ball.v += ball.a * dt
        ball.pos += ball.v * dt
        arr[0].pos, arr[1].pos, arr[2].pos, arr[3].pos = ball.pos, ball.pos, ball.pos, ball.pos
        arr[0].axis, arr[1].axis, arr[2].axis, arr[3].axis = (i * 3000000000000 for i in f)
    t += 1

scene.capture("simulation")
