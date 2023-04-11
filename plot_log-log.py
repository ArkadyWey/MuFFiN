import matplotlib 
from matplotlib import pyplot as plt
import numpy 

x = [1.0,2.0,3.0,4.0,5.0]
y = [1.8,0.92,0.62,0.46,0.36]

x = [0.02,0.04,0.06,0.08,0.10] # small-sweep
y = [84,42.5,28,21,17] # small-sweep

x_s = numpy.linspace(x[0],x[-1],100)
y_s = numpy.linspace(y[0],y[-1],100)

log_x = numpy.log(x) 
log_y = numpy.log(y)

log_x_s = numpy.log(x_s)
log_y_s = numpy.log(y_s)


m = -1.0
c = 0.6
m = -1.0
c = 0.525

plt.scatter(log_x, log_y)
plt.plot(log_x_s, m*log_x_s+c)

plt.show()

plt.scatter(x,y)
plt.plot(x_s,numpy.exp(c)*x_s**m)
print(numpy.exp(c))
# 1.8221188003905089 # large-sweep 
# 1.6904588483790914 # small-sweep

plt.show()


delt=0.5
epsi=0.1
alph=0.2
c = (1-alph*delt*epsi)**(1/(delt*epsi))
print(c)

