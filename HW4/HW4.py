import numpy as np
from vpython import *

A = 0.10    # Amplitude
N = 50      # Number of balls
d = 0.4     # Distance between two adjacent balls
m = 0.1     #  Mass of a ball
k = 10.0    # Force constant of springs

# Graph setting
kω_graph = graph(width = 1000, height = 500, title = 'Phonon Dispersion Relationship', xtitle = 'Wave number (k)', ytitle = 'Angular frequency (ω)')
p = gdots(color = color.blue, graph = kω_graph)

# Plotting
for n in range(1, int(N/2)):    # n from 1 to N/2-1

    # Wavevector = 2π/λ_n for every n
    Wavevector = 2 * pi / (N*d / n)

    # Initial phase, position & velocity of every ball
    phase = Wavevector * np.arange(N) * d
    ball_pos = np.arange(N) * d + A * np.sin(phase)
    ball_v = np.zeros(N)

    # Initial length of every spring
    spring_len = np.ones(N) * d

    t, dt = 0, 0.0003

    # When t < T/4
    while (ball_pos[1] - d > 0):
        t += dt

        # Setting length of every spring, the last and the first connected
        spring_len[:-1] = ball_pos[1:] - ball_pos[:-1]
        spring_len[-1] = ball_pos[0] - ball_pos[-1] + N*d

        # Setting velocity of every ball, the last and the first connected
        ball_v[1:] += k* (spring_len[1:]-d)/m*dt - k* (spring_len[:-1]-d)/m*dt
        ball_v[0] += k* (spring_len[0]-d)/m*dt - k* (spring_len[-1]-d)/m*dt

        # Setting position of every ball
        ball_pos += ball_v*dt
    
    p.plot(pos = (Wavevector, 2*pi/(t*4)))