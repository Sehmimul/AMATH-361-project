import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
import pylbm
import glob
import re
from PIL import Image
import json

X, Y, LA = sp.symbols('X, Y, LA')
rho, qx, qy = sp.symbols('rho, qx, qy')


def bc_in(f, m, x, y):
    m[qx] = rhoo * v0


def vorticity(sol):
    ux = sol.m[qx] / sol.m[rho]
    uy = sol.m[qy] / sol.m[rho]
    V = np.abs(uy[2:, 1:-1] - uy[0:-2, 1:-1] -
               ux[1:-1, 2:] + ux[1:-1, 0:-2])/(2*sol.domain.dx)
    return -V


def sort_filenames(temp_filenames):
    tails = []
    for temp_filename in temp_filenames:
        temp = re.findall(r'\d+', temp_filename)
        tails.append(int(temp[len(temp)-1]))

    filenames = [x for _, x in sorted(zip(tails, temp_filenames))]
    return filenames


def image_to_gif(mypath, gif_name, imagetype):
    frames = []
    filenames = sort_filenames(glob.glob(mypath + '/plot*.' + imagetype))
    for filename in filenames:
        frames.append(Image.open(filename))

    frames_per_sec = 20
    frames[0].save(mypath+'/'+gif_name, format='GIF', save_all=True,
                   append_images=frames, optimize=False, duration=(1000/frames_per_sec), loop=0)
    print('Gif creation done!')
    return 0

# 500000000
# parameters
config_file = "../config.json"
with open(config_file) as file:
    inputs = json.load(file)
print(inputs)

rayon = 0.05
Re = inputs['reynolds_no']
dx = 1./64   # spatial step
la = 1.      # velocity of the scheme
Tf = inputs['final_time']      # final time of the simulation
time = np.linspace(0, Tf, inputs['num_frames'])
v0 = la/20   # maximal velocity obtained in the middle of the channel
rhoo = 1.    # mean value of the density
# mu = 1.e-3   # bulk viscosity
mu = 0.001
eta = rhoo*v0*2*rayon/Re  # shear viscosity
# initialization
xmin, xmax, ymin, ymax = 0., 4., 0., 2.
dummy = 3.0/(la*rhoo*dx)
s_mu = 1.0/(0.5+mu*dummy)
s_eta = 1.0/(0.5+eta*dummy)
s_q = s_eta
s_es = s_mu
s = [0., 0., 0., s_mu, s_es, s_q, s_q, s_eta, s_eta]
dummy = 1./(LA**2*rhoo)
qx2 = dummy*qx**2
qy2 = dummy*qy**2
q2 = qx2+qy2
qxy = dummy*qx*qy

print("Reynolds number: {0:10.3e}".format(Re))
print("Bulk viscosity : {0:10.3e}".format(mu))
print("Shear viscosity: {0:10.3e}".format(eta))
print("relaxation parameters: {0}".format(s))

dico = {
    'box': {'x': [xmin, xmax],
            'y': [ymin, ymax],
            'label': [0, 2, 0, 0]
            },
    'elements': [pylbm.Circle([.3, 0.5*(ymin+ymax)+dx], rayon, label=1)],
    'space_step': dx,
    'scheme_velocity': la,
    'parameters': {LA: la},
    'schemes': [
        {
            'velocities': list(range(9)),
            'conserved_moments': [rho, qx, qy],
            'polynomials': [
                1, LA*X, LA*Y,
                3*(X**2+Y**2)-4,
                (9*(X**2+Y**2)**2-21*(X**2+Y**2)+8)/2,
                3*X*(X**2+Y**2)-5*X, 3*Y*(X**2+Y**2)-5*Y,
                X**2-Y**2, X*Y
            ],
            'relaxation_parameters': s,
            'equilibrium': [
                rho, qx, qy,
                -2*rho + 3*q2,
                rho-3*q2,
                -qx/LA, -qy/LA,
                qx2-qy2, qxy
            ],
        },
    ],
    'init': {rho: rhoo,
             qx: 0.,
             qy: 0.
             },
    'boundary_conditions': {
        0: {'method': {0: pylbm.bc.BouzidiBounceBack}, 'value': bc_in},
        1: {'method': {0: pylbm.bc.BouzidiBounceBack}},
        2: {'method': {0: pylbm.bc.NeumannX}},
    },
    'generator': 'cython',
}

sol = pylbm.Simulation(dico)
for i in range(0, len(time)):
    while sol.t < time[i]:
        sol.one_time_step()

    viewer = pylbm.viewer.matplotlib_viewer
    fig = viewer.Fig()
    ax = fig[0]
    im = ax.image(vorticity(sol).transpose(), clim=[-3., 0])
    ax.ellipse([.3/dx, 0.5*(ymin+ymax)/dx], [rayon/dx, rayon/dx], 'r')
    ax.title = 'Karman vortex street at t = {0:f} and Reynold number {1:f}'.format(sol.t,Re)
    plt.savefig(
        '../output/plot' + str(i) + '.png', format="png")
    plt.close()
# fig.show()

image_to_gif(mypath='../output/', gif_name='Plot.gif', imagetype='png')
