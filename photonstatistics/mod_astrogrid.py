"""
Generates several observations for PhotonStatistics analysis

"""

import numpy as np
import matplotlib.pyplot as plt

from medis.medis_main import RunMedis
from medis.utils import dprint
from medis.plot_tools import grid, quick2D
from mkidpipeline.hdf.photontable import Photontable

from photonstatistics.master import sp, mp, iop, atmp, tp, ap, TESTDIR

# product = 'fields'
product = 'photons'
# sp.numframes = 6000
sp.numframes = 1
sp.sample_time = 5e-3
TESTDIR = f'PhotonStatistics/200727/{sp.numframes}'
sp.num_processes = 1
sp.quick_companions = False
ap.companion = False
tp.use_aber = True
tp.add_zern = True
dist = np.arange(1,5) * 7/4  # 7 is max radial sep and 4 is number of evenly spaced sources
ap.companion_xy = np.hstack((
    np.vstack((dist, np.zeros((4)))),
    np.vstack((np.zeros((4)), dist)),
    -np.vstack((dist, np.zeros((4)))),
    -np.vstack((np.zeros((4)), dist))
 )).T
# ap.contrast = 10**np.repeat([-3.5,-4,-4.5,-5],4)
atmp.cn_sq = 5e-12
# ap.star_flux *= 20
ap.contrast = np.repeat([4, 2, 1, 0.5],4)*1e-4
ap.star_flux *= 0.1
sp.verbose = False
sp.debug = True

class mod():
    def __init__(self, num_samp=3):
        self.median_val = 50e-3
        self.multiplier = np.logspace(np.log10(0.2), np.log10(5), num_samp)[:1]
        self.vals = self.multiplier * self.median_val

if __name__ == '__main__':
    metric_config = mod()
    for i, val in enumerate(metric_config.vals):
        tp.satelite_speck['period'] = val
        name = f'{TESTDIR}/{val}'
        sim = RunMedis(name=name, product=product)
        observation = sim()

        if product == 'fields':
            grid(observation['fields'], show=False)#, vlim=(-2e-7,2e-7))

        elif product == 'photons':
            grid(sim.cam.rebin_list(observation['photons']), show=False)

            # to look at the photontable
            obs = Photontable(iop.photonlist)
            print(obs.photonTable)
            # to plot an image of all the photons on the array
            image = obs.getPixelCountImage(integrationTime=None)['image']
            quick2D(image, show=False, title=f'{val}')

    plt.show(block=True)

