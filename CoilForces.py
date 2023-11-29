from MagCoil import MagCoil
from pylab import *

N1=9*9+7*7
N2=N1
I=50.
dz=0.05335*2
R=(29.09+34.35)/400
smidge=array([1,1,1])*dz*1e-6

z1=-1*dz/2
r1=R
c1=MagCoil(array([0.,0.,z1]), array([0,0,1.0]), R=r1, I=N1*I)

z2=dz/2
r2=R
c2=MagCoil(array([0.,0.,z2]), array([0,0,1.0]), R=r2, I=N2*I)

B=c1.B(c1.r0)
print('Bctr={:0.2f}T'.format(B[0,2]))
B=c1.B(c2.r0+array([c2.R,0,0]))
print('B at other coil={}'.format(B))
Br=B[0,0]
F2=2*pi*c2.R* N2*I * Br

print('Force on coil 2 is {} N ({} lb)'.format(F2,F2*.224809))
Bctr=c1.B(c1.r0+smidge)
Bchk=c1.mu * c1.R**2 * N2*I /(2*c1.R**3)
print('Coil Center check: {} T, {} T'.format(Bctr[0,2],Bchk))

Bnet=c1.B(c1.r0+smidge)+c2.B(c1.r0+smidge)
print(Bnet)
print('Coil Center net: {} T'.format(Bnet[0,2]))

n_bar=3
F_bar=F2/n_bar
endfactor=1.0 # ends can't displace but can rotate/pivot
E=193e9  #Modulus of elasticity, Pa
w2=2*.0254 # outer width of box beam, m
h2=.375*.0254 # outer height of box beam, m
thick=h2/2 # solid # wall thickness of box beam, m
w1=w2-2*thick
h1=h2-2*thick
I=(w2 * h2**3 /12) - (w1 * h1**3 /12) # Moment of inertia
A=w2*h2-w1*h1
yieldstress=290e6 # MPa
F_yield=yieldstress*A
F_bukl=endfactor * pi**2 * E * I / dz**2 # Euler's column formula
print("*****************************")
print("{:.3f}m spacing".format(dz))
print("{:.3g} N force".format(F_bar))
print("{:.2f}% of buckling".format(F_bar/F_bukl*100))
print("{:.1f}% of yield".format(F_bar/F_yield*100, dz))



