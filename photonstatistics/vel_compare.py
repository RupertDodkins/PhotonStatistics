"""
Generates several observations for PhotonStatistics analysis

"""

import numpy as np
import matplotlib.pyplot as plt

from medis.medis_main import RunMedis
from medis.utils import dprint
from medis.plot_tools import grid, quick2D
from mkidpipeline.hdf.photontable import ObsFile

from photonstatistics.master import sp, mp, iop, atmp, TESTDIR

# product = 'fields'
product = 'photons'

sp.numframes = 2000
sp.sample_time = 5e-3
TESTDIR = f'PhotonStatistics/vel_compare_5ms/{sp.numframes}'
sp.num_processes = 10

class vel():
    def __init__(self, num_samp=3):
        self.median_val = 10
        # self.multiplier = np.logspace(np.log10(0.1), np.log10(10), num_samp)
        self.multiplier = np.array([0])
        self.vals = self.multiplier * self.median_val

if __name__ == '__main__':
    metric_config = vel()
    for i, val in enumerate(metric_config.vals):
        atmp.vel = val
        name = f'{TESTDIR}/{val}'
        sim = RunMedis(name=name, product=product)
        observation = sim()

        if product == 'fields':
            grid(observation['fields'], show=False)#, vlim=(-2e-7,2e-7))

        elif product == 'photons':
            grid(sim.cam.rebin_list(observation['photons']), show=False)

            # to look at the photontable
            obs = ObsFile(iop.photonlist)
            print(obs.photonTable)
            # to plot an image of all the photons on the array
            image = obs.getPixelCountImage(integrationTime=None)['image']
            quick2D(image, show=False, title=f'{val}')

    plt.show(block=True)

