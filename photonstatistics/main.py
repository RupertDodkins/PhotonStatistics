"""
Generates observations for PhotonStatistics analysis

"""

import numpy as np
import matplotlib.pyplot as plt

from medis.medis_main import RunMedis
from medis.utils import dprint
from medis.plot_tools import grid

from photonstatistics.master import sp, mp, iop, atmp

sp.numframes = 5
# atmp.model = 'single'
atmp.model = 'hcipy_standard'

TESTDIR = f'PhotonStatistics/{sp.numframes}'
name = f'{TESTDIR}/{atmp.model}'
# product = 'photons'
# product = 'rebinned_cube'
product = 'fields'

sp.verbose = True
# sp.debug = True

if __name__ == '__main__':
    sp.quick_detect = False
    mp.hot_counts = False
    mp.dark_counts  = False
    mp.bad_pix = True
    sim = RunMedis(name=name, product=product)
    observation = sim()
    print(observation.keys(), )

    if product == 'rebinned_cube':
        grid(observation['rebinned_cube'], vlim= (0,3))
    elif product == 'photons':
        grid(sim.sim.rebin_list(observation['photons'])[::100], vlim= (0,3))
        # plt.hist(observation['photons'][0])
        # plt.show()
    else:
        dprint(np.sum(np.abs(np.sum(observation['fields'][:, -1, :, :], axis=2)) ** 2))
        grid(observation['fields'])

    if product == 'photons':
        from mkidpipeline.hdf.photontable import ObsFile

        # to look at the photontable
        obs = ObsFile(iop.photonlist)
        print(obs.photonTable)
        # to plot an image of all the photons on the array
        image = obs.getPixelCountImage(integrationTime=None)['image']
        plt.imshow(image)
        plt.show(block=True)