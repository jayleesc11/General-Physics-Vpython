from vpython import *
import numpy as np
from histogram import *

N = 200
m, size = 4E-3 / 6E23, 31E-12*10                # He atom are 10 times bigger for easiear collision but not too big for accuracy
L = ((24.4E-3/(6E23))*N)**(1/3.0) / 2 + size    # 2L is the cubic container's original length, width, and height
k, T = 1.38E-23, 298.0                          # Boltzmann Constant and initial temperature
t, dt = 0, 3E-13
momentum = 0
p, V = 0, 0
vrms = (2*k*1.5*T/m)**0.5                       # the initial root mean square velocity
stage = 0                                       # stage number
atoms = []                                      # list to store atoms

# histogram setting
deltav = 50. ## slotwidth for v histogram
vdist = graph(x=800, y=0, ymax = N*deltav/1000.,width=500, height=300, xtitle='v', ytitle='dN', align = 'left')
## plot of the curve for the atom theoretical speed distribution
theory_low_T = gcurve(color=color.cyan)
theory_high_T = gcurve(color=color.green)
dv = 10.
for v in arange(0.,4201.+dv,dv):
    theory_low_T.plot(pos=(v,(deltav/dv)*N*4.*pi*((m/(2.*pi*k*T))**1.5)*exp((-0.5*m*v**2)/(k*T))*(v**2)*dv))
## plot the simulation speed distribution
observation1 = ghistogram(graph = vdist, bins=arange(0.,4200.,deltav), color=color.red)
observation2 = ghistogram(graph = vdist, bins=arange(0.,4200.,deltav), color=color.blue)

# keyboard control setting
def keyinput(evt):
    global stage
    tap = {'n': 1}
    s = evt.key

    if s in tap:
        stage += tap[s]
        if stage <= 3:
            print("stage", stage)
        if stage == 2:
            for v in arange(0.,4201.+dv,dv):
                theory_high_T.plot(pos=(v,(deltav/dv)*N*4.*pi*((m/(2.*pi*k*T))**1.5)*exp((-0.5*m*v**2)/(k*T))*(v**2)*dv))

# initialization
scene = canvas(width=500, height=500, background=vector(0.2,0.2,0), align = 'left')
scene.bind('keydown', keyinput)
container = box(length = 2*L, height = 2*L, width = 2*L, opacity=0.2, color = color.yellow )
p_a, v_a = np.zeros((N,3)), np.zeros((N,3)) # particle position array and particle velocity array, N particles and 3 for x, y, z
v_W = L / (20000.0*dt)

for i in range(N):
    p_a[i] = [2 * L*random() - L, 2 * L*random() - L, 2 * L*random() - L] # particle is initially random positioned in container
    if i == N-1: # the last atom is with yellow color and leaves a trail
        atom = sphere(pos=vector(p_a[i, 0], p_a[i, 1], p_a[i, 2]), radius = size, color=color.yellow, make_trail = True, retain = 50)
    else: # other atoms are with random color and leaves no trail
        atom = sphere(pos=vector(p_a[i, 0], p_a[i, 1], p_a[i, 2]), radius = size, color=vector(random(), random(), random()))
    ra = pi*random()
    rb = 2*pi*random()
    v_a[i] = [vrms*sin(ra)*cos(rb), vrms*sin(ra)*sin(rb), vrms*cos(ra)] # particle initially same speed but random direction
    atoms.append(atom)

# calculate velocity after collision
def vcollision(a1p, a2p, a1v,a2v):
    v1prime = a1v - (a1p - a2p) * sum((a1v-a2v)*(a1p-a2p)) / sum((a1p-a2p)**2)
    v2prime = a2v - (a2p - a1p) * sum((a2v-a1v)*(a2p-a1p)) / sum((a2p-a1p)**2)
    return v1prime, v2prime

while True:
    t += dt
    rate(10000)

    # calculate T
    K = 0
    for i in range(N):
        K += m*(v_a[i][0]**2 + v_a[i][1]**2 + v_a[i][2]**2) / 2
    T = K / (3/2*N*k)

    # display new positions for all atoms
    p_a += v_a*dt 
    for i in range(N):
        atoms[i].pos = vector(p_a[i, 0], p_a[i, 1], p_a[i, 2])
    
    # find collisions between pairs of atoms, and handle their collisions
    r_array = p_a-p_a[:,np.newaxis] # array for vector from one atom to another atom for all pairs of atoms
    rmag = np.sqrt(np.sum(np.square(r_array),-1)) # distance array between atoms for all pairs of atoms
    hit = np.less_equal(rmag,2*size)-np.identity(N) # if smaller than 2*size meaning these two atoms might hit each other
    hitlist = np.sort(np.nonzero(hit.flat)[0]).tolist() # change hit to a list
    for ij in hitlist: # i,j encoded as i*Natoms+j
        i, j = divmod(ij,N) # atom pair, i-th and j-th atoms, hit each other
        hitlist.remove(j*N+i) # remove j,i pair from list to avoid handling the collision twice
        if sum((p_a[i]-p_a[j])*(v_a[i]-v_a[j])) < 0 : # only handling collision if two atoms are approaching each other
            v_a[i], v_a[j] = vcollision(p_a[i], p_a[j], v_a[i], v_a[j]) # handle collision
    
    # find collisions between the atoms and the walls, and handle their elastic collisions
    for i in range(N):
        if abs(p_a[i][0]) >= container.length/2 - size and p_a[i][0]*v_a[i][0] > 0 :
            if stage != 1:
                v_a[i][0] = - v_a[i][0]
                momentum += 2*m*abs(v_a[i][0])
            else:
                if v_a[i][0] > 0:
                    momentum += 2*m*abs(v_W + v_a[i][0])
                    v_a[i][0] = -v_a[i][0] - 2*v_W
                else:
                    momentum += 2*m*abs(v_W - v_a[i][0])
                    v_a[i][0] = -v_a[i][0] + 2*v_W

        if abs(p_a[i][1]) >= L - size and p_a[i][1]*v_a[i][1] > 0 :
            v_a[i][1] = - v_a[i][1]
            momentum += 2*m*abs(v_a[i][1])
        if abs(p_a[i][2]) >= L - size and p_a[i][2]*v_a[i][2] > 0 :
            v_a[i][2] = - v_a[i][2]
            momentum += 2*m*abs(v_a[i][2])

    # to-do in different stage
    if stage == 0:
        observation1.plot(data = np.sqrt(np.sum(np.square(v_a),-1)))
    elif stage == 1 :
        container.length -= 2* v_W *dt
        if container.length <= L:
            stage = 2
            print("stage", stage)
            for v in arange(0.,4201.+dv,dv):
                theory_high_T.plot(pos=(v,(deltav/dv)*N*4.*pi*((m/(2.*pi*k*T))**1.5)*exp((-0.5*m*v**2)/(k*T))*(v**2)*dv))
    elif stage == 2:
        observation2.plot(data = np.sqrt(np.sum(np.square(v_a),-1)))
    else:
        container.length = 2*L
    
    # print p, V, T
    if t >= 1000*dt:
        p = momentum / t / (2*container.length*container.width + 2*container.length*container.height + 2*container.width*container.height)
        V = container.length * container.width * container.height
        print("T =", "{:.2f}".format(T), ", p =", "{:.2e}".format(p), ", V =", "{:.2e}".format(V), ", pV =", "{:.2e}".format(p*V), ", NkT =", "{:.2e}".format(N*k*T), ", pV^(5/3) =", "{:.2e}".format(p*V**(5/3)))

        t = 0
        momentum = 0