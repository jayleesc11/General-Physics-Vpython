from vpython import *
from diatomic import *

N = 20                                  # Number of molecules
L = ((24.4E-3/(6E23))*N)**(1/3.0)/50    # Half of the length of the cubic container box
m = 14E-3/6E23                          # Average mass of O and C

# Some constants to set up the initial speed
k = 1.38E-23                ## Boltzmann constant
T = 298.0                   ## Temperature
initial_v = (3*k*T/m)**0.5

# Scene initialization
scene = canvas(width = 400, height =400, align = 'left', background = vec(1, 1, 1))
container = box(length = 2*L, height = 2*L, width = 2*L, opacity = 0.4, color = color.yellow )

# Plots initialization
energies = graph(width = 600, align = 'left', ymin=0)
c_avg_com_K = gcurve(color = color.green)
c_avg_v_P = gcurve(color = color.red)
c_avg_v_K = gcurve(color = color.purple)
c_avg_r_K = gcurve(color = color.blue)

# CO molecules initialization
COs = []
for i in range(N):
    O_pos = vec(random()-0.5, random()-0.5, random()-0.5) * L                   ### random initial position of O
    CO = CO_molecule(pos = O_pos, axis = vector(d, 0, 0)) 
    CO.C.v = vector(initial_v*random(), initial_v*random(), initial_v*random()) ### random initial velocity of C
    CO.O.v = vector(initial_v*random(), initial_v*random(), initial_v*random()) ### random initial velocity of O
    COs.append(CO)

# Simulation

## Loop counter
times = 0

## Time
t = 0
dt = 5E-16

## Total energy
total_com_K = 0
total_v_K = 0
total_v_P = 0
total_r_K = 0

while True:
    rate(3000)
    times += 1
    t += dt

    ## Modify pos, v, a, ... of CO
    for CO in COs:
        CO.time_lapse(dt)

    ## Collision between molecules
    for i in range(N-1):        ### the first N-1 molecules
        for j in range(i+1,N):  ### from i+1 to the last molecules (avoid double checking)
            if mag(COs[i].C.pos - COs[j].C.pos) <= 2*size and dot(COs[i].C.pos - COs[j].C.pos, COs[i].C.v - COs[j].C.v) <= 0 :
                (COs[i].C.v, COs[j].C.v) = collision(COs[i].C, COs[j].C)
            if mag(COs[i].C.pos - COs[j].O.pos) <= 2*size and dot(COs[i].C.pos - COs[j].O.pos, COs[i].C.v - COs[j].O.v) <= 0 :
                (COs[i].C.v, COs[j].O.v) = collision(COs[i].C, COs[j].O)
            if mag(COs[i].O.pos - COs[j].C.pos) <= 2*size and dot(COs[i].O.pos - COs[j].C.pos, COs[i].O.v - COs[j].C.v) <= 0 :
                (COs[i].O.v, COs[j].C.v) = collision(COs[i].O, COs[j].C)
            if mag(COs[i].O.pos - COs[j].O.pos) <= 2*size and dot(COs[i].O.pos - COs[j].O.pos, COs[i].O.v - COs[j].O.v) <= 0 :
                (COs[i].O.v, COs[j].O.v) = collision(COs[i].O, COs[j].O)
    
    ## Collision between molecule and wall
    for CO in COs:
        if (CO.C.pos.x <= -(L-size) and CO.C.v.x <= 0) or (CO.C.pos.x >= L-size and CO.C.v.x >= 0) :
            CO.C.v.x = -CO.C.v.x
        if (CO.C.pos.y <= -(L-size) and CO.C.v.y <= 0) or (CO.C.pos.y >= L-size and CO.C.v.y >= 0) :
            CO.C.v.y = -CO.C.v.y
        if (CO.C.pos.z <= -(L-size) and CO.C.v.z <= 0) or (CO.C.pos.z >= L-size and CO.C.v.z >= 0) :
            CO.C.v.z = -CO.C.v.z
        if (CO.O.pos.x <= -(L-size) and CO.O.v.x <= 0) or (CO.O.pos.x >= L-size and CO.O.v.x >= 0) :
            CO.O.v.x = -CO.O.v.x
        if (CO.O.pos.y <= -(L-size) and CO.O.v.y <= 0) or (CO.O.pos.y >= L-size and CO.O.v.y >= 0) :
            CO.O.v.y = -CO.O.v.y
        if (CO.O.pos.z <= -(L-size) and CO.O.v.z <= 0) or (CO.O.pos.z >= L-size and CO.O.v.z >= 0) :
            CO.O.v.z = -CO.O.v.z
    
    ## Plotting avg_com_K, avg_v_K, avg_v_P, and avg_r_K
    for CO in COs:
        total_com_K += CO.com_K() * dt
        c_avg_com_K.plot(t, total_com_K / t)
        total_v_K += CO.v_K() * dt
        c_avg_v_K.plot(t, total_v_K / t)
        total_v_P += CO.v_P() * dt
        c_avg_v_P.plot(t, total_v_P / t)
        total_r_K += CO.r_K() * dt
        c_avg_r_K.plot(t, total_r_K / t)