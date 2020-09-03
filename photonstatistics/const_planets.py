"""
Generates several observations for PhotonStatistics analysis -- this time focusing on generating the planet fluxes in
the way Alex/Clint did in their paper

"""

import numpy as np
import matplotlib.pyplot as plt

from medis.medis_main import RunMedis
from medis.MKIDS import Camera
from medis.utils import dprint
from medis.plot_tools import grid, quick2D
from mkidpipeline.hdf.photontable import Photontable

from photonstatistics.master import sp, mp, iop, atmp, tp, ap

product = 'fields'
# product = 'photons'
sp.numframes = 6001
# sp.numframes = 5
sp.sample_time = 5e-3
TESTDIR = f'PhotonStatistics/200902/{sp.numframes}'
sp.num_processes = 10
sp.quick_companions = True
ap.companion = True
tp.use_aber = True
tp.add_zern = True
tp.satelite_speck['period'] = False
dist = np.arange(1,5) * 7/4  # 7 is max radial sep and 4 is number of evenly spaced sources
ap.companion_xy = np.hstack((
    np.vstack((dist, np.zeros((4)))),
    np.vstack((np.zeros((4)), dist)),
    -np.vstack((dist, np.zeros((4)))),
    -np.vstack((np.zeros((4)), dist))
 )).T

atmp.cn_sq = 5e-12
# ap.star_flux *= 20
ap.contrast = np.repeat([4, 2, 1, 0.5],4)*1e-4
ap.star_flux *= 0.1
sp.verbose = True
sp.debug = False


if __name__ == '__main__':
    sim = RunMedis(name=TESTDIR, product='fields')
    observation = sim()
    for ichunk in range(int(np.ceil(sim.tel.num_chunks))):

        if ichunk == 0:
            fields = observation['fields']
        else:
            fields = sim.tel()['fields']

        abs_step = ichunk*sim.tel.chunk_steps

        # generate photons just for the star
        cam = Camera(usesave=False, product='photons')
        observation = cam(fields[:,:,:,:1], abs_step=abs_step, finalise_photontable=False)
        star_photons = observation['photons']#[[0,1,3]]

        # select detector plane and planets
        mean_planet_map = np.mean(np.abs(fields[:, -1, :, -1]) ** 2, axis=0)  # assumes one object from quick_companions
        mean_planet_map = np.repeat(mean_planet_map,len(fields), axis=0)[:,np.newaxis]
        if mp.QE_var: mean_planet_map *= mp.QE_map.T
        mean_planet_map = cam.rescale_cube(mean_planet_map)
        mean_planet_map = mean_planet_map[:, 0] * ap.star_flux * sp.sample_time  # assumes one wavelength
        poisson_stream = np.random.poisson(mean_planet_map)
        coords = np.array(np.where(np.ones_like(poisson_stream))).reshape(len(mean_planet_map.shape),*mean_planet_map.shape)
        planet_photons = []
        times, rows, cols = poisson_stream.shape
        for t in range(times):
            for r in range(rows):
                for c in range(cols):
                    if poisson_stream[t, r, c] > 0:
                        pix_photons = np.array(poisson_stream[t, r, c] * list(coords[:,t, r, c])).reshape(-1,3)
                        # print(poisson_stream[t, r, c], coords[:, t, r, c], poisson_stream[t, r, c] * list(coords[:, t, r, c]), pix_photons)
                        for photon in pix_photons:
                            # print(photon)
                            planet_photons.append(photon)

        planet_photons = np.array(planet_photons).T.astype(np.float32)
        planet_photons = np.insert(planet_photons, obj=1, values=cam.phase_cal(ap.wvl_range[0]), axis=0)
        planet_photons[0] = (planet_photons[0] + abs_step) * sp.sample_time
        photons = np.concatenate((star_photons, planet_photons), axis=1)

        # cam.save_photontable(photonlist=photons, index=None, populate_subsidiaries=False)
        stem = cam.arange_into_stem(photons.T, (cam.array_size[1], cam.array_size[0]))
        stem = list(map(list, zip(*stem)))
        stem = cam.remove_close(stem)
        photons = cam.ungroup(stem)
        photons = photons[[0,1,3,2]]
        # grid(cam.rebin_list(photons), show=False)
        cam.populate_photontable(photons=photons, finalise=False)
    cam.populate_photontable(photons=[], finalise=True)
    grid(cam.rebin_list(photons), show=False)

    # to look at the photontable
    obs = Photontable(iop.photonlist)
    print(obs.photonTable)

    # to plot an image of all the photons on the array
    image = obs.getPixelCountImage(integrationTime=None)['image']
    quick2D(image, show=False, title='Const planet photons')

    plt.show(block=True)

