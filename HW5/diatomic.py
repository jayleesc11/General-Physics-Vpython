from vpython import *

# Constant about CO
size = 31E-12                       # Atomic radius
m_o, m_c = 16.0/6E23, 12.0/6E23     # Atomic mass
k_bond = 18600.0                    # Spring constant
d = 2.5*size                        # Spring length
dt = 1E-16

class CO_molecule:
    def __init__(self, pos, axis):
        self.O = sphere(pos = pos, radius = size, color = color.red)
        self.C = sphere(pos = pos + axis, radius = size, color = color.blue)
        self.bond = cylinder(pos = pos, axis = axis, radius = size/2.0, color = color.white)
        self.O.m = m_o
        self.C.m = m_c
        self.O.v = vector(0, 0, 0)
        self.C.v = vector(0, 0, 0)
        self.bond.k = k_bond

    def bond_force_on_O(self):
        return self.bond.k*(mag(self.bond.axis)-d)*norm(self.bond.axis)
    
    def time_lapse(self, dt): # Calculate a, v, and pos of C & O, and bond's pos and axis after dt
        self.C.a = - self.bond_force_on_O() / self.C.m
        self.O.a = self.bond_force_on_O() / self.O.m
        self.C.v += self.C.a * dt
        self.O.v += self.O.a * dt
        self.C.pos += self.C.v * dt
        self.O.pos += self.O.v * dt
        self.bond.axis = self.C.pos - self.O.pos
        self.bond.pos = self.O.pos

    def com(self): # Return position of center of mass
        return (m_o * self.O.pos + m_c * self.C.pos)/(m_o + m_c)

    def com_v(self): # Return velocity of center of mass
        return (m_o * self.O.v + m_c * self.C.v)/(m_o + m_c)

    def v_P(self): # return potential energy of the bond for the vibration motion
        return 1/2 * k_bond * (mag(self.bond.axis) - d) ** 2

    def v_K(self): # Return kinetic energy of the vibration motion
        v_K_c = 1/2 * m_c * mag2((self.C.v - self.com_v()).proj(self.bond.axis))
        v_K_o = 1/2 * m_o * mag2((self.O.v - self.com_v()).proj(self.bond.axis))
        return v_K_c + v_K_o
    
    def r_K(self): # Return kinetic energy of the rotational motion
        internal_t_K = 1/2 * m_c * m_o / (m_c + m_o) * mag2(self.C.v - self.O.v)
        return internal_t_K - self.v_K()
    
    def com_K(self): # Return kinetic energy of the translational motion of the center of mass
        return 1/2 * (m_c + m_o) * mag2(self.com_v())
    
def collision(a1, a2):
    v1prime = a1.v - 2 * a2.m/(a1.m + a2.m) * (a1.pos-a2.pos) * dot (a1.v - a2.v, a1.pos - a2.pos) / mag2(a1.pos - a2.pos)
    v2prime = a2.v - 2 * a1.m/(a1.m + a2.m) * (a2.pos-a1.pos) * dot (a2.v - a1.v, a2.pos - a1.pos) / mag2(a2.pos - a1.pos)
    return v1prime, v2prime

if __name__ == '__main__':
    a = CO_molecule(pos=vector(0, 0, 0), axis = vector(2.6*size, 0, 0))
    a.O.v = vector(1.0, 1.0, 0)
    a.C.v = vector(2.0, -1.0, 0)
    a.time_lapse(dt)
    print(a.bond_force_on_O(), a.com(), a.com_v(), a.v_P(), a.v_K(), a.O, a.com_K())