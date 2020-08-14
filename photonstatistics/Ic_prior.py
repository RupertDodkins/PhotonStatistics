"""
Generate an Ic map to seed bin-free SSD as prior

"""
import os
import numpy as np
import matplotlib.pyplot as plt

from medis.medis_main import RunMedis
from medis.MKIDS import Camera
from medis.utils import dprint
from medis.plot_tools import grid, quick2D
from mkidpipeline.hdf.photontable import Photontable

from photonstatistics.master import sp, mp, iop, atmp, tp, ap, TESTDIR

import pickle
from pprint import pprint

with open('/mnt/data0/dodkins/MEDIS_photonlists/PhotonStatistics/200709/6000/params.pkl', 'rb') as handle:
    params07 = pickle.load(handle)

with open('/mnt/data0/dodkins/MEDIS_photonlists/PhotonStatistics/200616/6000/0.010000000000000002/params.pkl', 'rb') as handle:
    params06 = pickle.load(handle)

for param06, param07 in zip(params06.values(), params07.values()):
    print(f'\n\t {param06.__name__()}')
    pprint(param06.__dict__)
    pprint(param07.__dict__)
# print(params)

# product = 'fields'
product = 'rebinned_cube'
sp.numframes = 6000
sp.sample_time = 5e-3
TESTDIR = f'PhotonStatistics/200709/{sp.numframes}'
sp.num_processes = 10
# sp.quick_companions = True
# dist = np.arange(1,5) * 7/4  # 7 is max radial sep and 4 is number of evenly spaced sources
# ap.companion_xy = np.hstack((
#     np.vstack((dist, np.zeros((4)))),
#     np.vstack((np.zeros((4)), dist)),
#     -np.vstack((dist, np.zeros((4)))),
#     -np.vstack((np.zeros((4)), dist))
#  )).T
# # ap.contrast = 10**np.repeat([-3.5,-4,-4.5,-5],4)
atmp.cn_sq = 5e-11
# # ap.star_flux *= 20
# ap.contrast = np.repeat([4, 2, 1, 0.5],4)*1e-4
ap.companion = False
# tp.use_atmos = False
tp.use_ao = True
ap.star_flux *= 0.1
# sp.debug = True
sp.quick_detect = False

name = f'{TESTDIR}'
sim = RunMedis(name=name, product='fields')
observation = sim()
# grid(observation['fields'], show=False, nstd=5)#, vlim=(-2e-7,2e-7))
cam = Camera(usesave=sp.save_to_disk, product=product)
# fields = [observation['fields'][0]]*100
# fields = np.repeat(observation['fields'], 100, 0)
# dprint(fields.shape)
observation = cam(observation['fields'])
# grid(cam.rebinned_cube)
Ic = np.sum(cam.rebinned_cube, axis=(0,1))
np.save(os.path.join(iop.testdir, 'Ic.npy'), Ic)
quick2D(Ic)
Ic = np.load(os.path.join(iop.testdir, 'Ic.npy'))
quick2D(Ic)