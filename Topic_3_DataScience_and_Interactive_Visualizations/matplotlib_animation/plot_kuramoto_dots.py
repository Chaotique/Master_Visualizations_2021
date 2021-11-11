import numpy as np
from scipy.integrate import odeint
import scipy
from numpy import random as rnd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as manimation

# setup video writer
FFMpegWriter = manimation.writers['ffmpeg']
metadata = dict(title='Movie Test2', artist='Matplotlib',
                comment='Movie support!')
writer = FFMpegWriter(fps=10, metadata=metadata)

# set parameters
n_osc = 50
y0 = rnd.rand(n_osc)*2*np.pi
omg = 0*np.sort(rnd.randn(n_osc))/10.
colors_omg = omg - min(omg)
colors_omg =np.linspace(0,1,n_osc, endpoint = False)#/= max(colors_omg)
omg -= np.mean(omg)
eps = 0.1
n_times  = 1000
t = np.linspace(0, 100. ,n_times)

# kuramoto right hand side
def func(y, t):
    xs = np.sum(np.sin(y))
    xc = np.sum(np.cos(y))
    return omg + eps/n_osc*(xs*np.cos(y)-xc*np.sin(y)) 

# integrate phases in time
y = odeint(func, y0, t)
# extract initial conditions for plotting
x0 = np.cos(y[0, :])
y0 = np.sin(y[0, :])
xc0 = np.zeros(0)
xs0 = np.zeros(0)

# setup canvas, add line for order parameter = 1
fig = plt.figure(figsize = (2,2))
plt.plot(np.cos(np.linspace(0., 2.*np.pi, 100)), np.sin(np.linspace(0., 2.*np.pi, 100)), color = (0.8,0.8,0.8))
plt.axis('off')
plt.xlim(-1.05, 1.05)
plt.ylim(-1.05, 1.05)


def plot(osci):
    """
    plotting function that will be called for eachtime point and for each oscillator
    """
    return plt.plot(x0[osci], y0[osci], 'o', 
               color =(np.abs(colors_omg[osci]%1.),0., 
               1.-np.abs(colors_omg[osci]%1.)),
               fillstyle='full', 
               markeredgecolor='red', 
               markeredgewidth=0.0,
               markersize = 4)

def plot_R():
    """
    plots order parameter at each time point
    """
    return plt.plot(xc0, xs0, 'k', lw = 1, markersize = 1)

# print current time 
time_text = plt.text(0.5, -0.5, '', verticalalignment='bottom', horizontalalignment='right',
        color=(0,0.3, 0.6), fontsize=10)

# create line for each oscillator
l_R, = plot_R()
l_o = list(np.zeros(n_osc))
for osci in range(n_osc):
    l_o[osci], = plot(osci)

#x0 = np.zeros(n_osc)
#y0 = np.zeros(n_osc)
with writer.saving(fig, "animate_kuramoto.mp4", n_times):
    global mt
    for i in range(n_times):
        for osci in np.arange(n_osc):
            x0[osci] = np.cos(y[i, osci])
            y0[osci] = np.sin(y[i, osci])
        xc0 = np.append(xc0, np.sum(x0)/n_osc)
        xs0 = np.append(xs0, np.sum(y0)/n_osc)
        if i%10==9:
            time_text.set_text(r'$R=$'+str(round(np.sqrt(np.sum(x0)**2 + np.sum(y0)**2)/n_osc, 2)))
        l_R.set_data(xc0, xs0)
        for osci in range(n_osc):
            l_o[osci].set_data(x0[osci], y0[osci])
        writer.grab_frame()

