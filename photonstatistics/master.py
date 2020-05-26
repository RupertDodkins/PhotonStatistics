import os
import numpy as np
from os.path import expanduser

from medis.params import sp, ap, tp, mp, iop, atmp

# sp.numframes = 2000 #2000 #500
sp.checkpointing = None
ap.companion_xy = [[2,0]]
ap.contrast = [1e-4]
ap.companion = True
ap.n_wvl_init = 1
ap.n_wvl_final = 1
tp.cg_type = 'Solid'
sp.sample_time = 0.5e-3
sp.grid_size = 512
ap.star_flux = 1.1*1e8
tp.satelite_speck['apply'] = True
tp.satelite_speck['amp'] = 12e-10
sp.beam_ratio = 0.15
tp.prescription = 'general_telescope' #'Subaru_SCExAO'  #
tp.obscure = False
tp.use_ao = True
sp.save_to_disk = False
sp.debug = False
tp.ao_act = 50
mp.array_size = np.array([140, 144])
atmp.cn_sq = 0.5e-11
# sp.skip_planes = ['coronagraph']
atmp.correlated_sampling = False
# atmp.model = 'hcipy_standard'
sp.quick_detect = False
mp.hot_counts = False
mp.dark_counts = False
mp.bad_pix = True
atmp.model = 'single'
sp.save_sim_object = False
sp.save_to_disk = True
sp.debug = False

TESTDIR = 'PhotonStatistics'

home = expanduser("~")
if home == '/Users/dodkins':
    iop.update_datadir('/Users/dodkins/MEDIS_photonlists/')
    mode = 'develop'
elif home == '/home/dodkins':
    # os.environ["DISPLAY"] = "/home/dodkins"
    iop.update_datadir('/mnt/data0/dodkins/MEDIS_photonlists/')
    mode = 'test'
else:
    print('System not recognised. Make sure $WORKING_DIR is set')
    raise SyntaxError

# mode = 'develop'
mode = 'test'
if mode == 'develop':
    sp.num_processes = 1
    sp.numframes = 5  # 2000 #500
elif mode == 'test':
    sp.num_processes = 10
    sp.numframes = 2000  # 2000 #500
else:
    raise SyntaxError

# iop.update_datadir('/mnt/data0/dodkins/MKIDSim/')
# sp.numframes = 5
# sp.num_processes = 1
# atmp.model = 'single'
# atmp.model = 'hcipy_standard'
sp.skip_planes = ['CPA','NCPA']  # ['wfs', 'deformable mirror']  # list of locations in optics train to save

TESTDIR = f'PhotonStatistics/{sp.numframes}'

