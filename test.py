#%%
import requests
from astropy.io import fits ,ascii
import os 
import argparse
import numpy as np
import matplotlib.pyplot as plt
# import glob
from astropy.time import Time
from datetime import timedelta #datetime
import matplotlib.gridspec as gridspec 
import matplotlib as mpl
from scipy.interpolate import interp1d
import subprocess
from astropy import units as u
from astropy import coordinates
# import getopt
import pandas as pd
from astropy.utils.exceptions import AstropyWarning
import warnings
warnings.filterwarnings("ignore",category=UserWarning)
warnings.simplefilter('ignore',category=AstropyWarning)
from astropy.coordinates import SkyCoord
#from astropy.coordinates import Galactic, FK5
# import pdb # for debugging purposes
from query_eso_archive import query_simbad
from ecmwf_utilities import request_ecmwf
#from astropy.utils.iers import conf
#conf.auto_max_age = None
import re
from astroquery.eso import Eso
from pathlib import Path

import numpy as np
from astropy.io import fits
import os

#%%



#%%
# for night in compressed_folders:
#     print(night)
#     files = os.listdir(os.path.join(compressed_folder, night))
#     for file in files:
#         print(file)
#         filename_in  = os.path.join(compressed_folder, night, file)
#         filename_out = os.path.join(compressed_folder, night, file.rsplit(".", 1)[0])
#         print(filename_in)
#         print(filename_out)
#         with open(filename_in, 'rb') as fh:
#             hdr = fits.HDUList.fromstring(unlzw(fh.read()))
#         # writing hdr to a file
#         # hdr.writeto(filename_in.rsplit(".", 1)[0], overwrite=True)
#         hdr.writeto(filename_out, overwrite=True)

#%%

# filepath = os.path.join(local_path, night)
# if os.path.exists(filepath):
#     print('Overwriting', filepath)

filename_in  = 'E:/ESO/Data/SPHERE/SPARTA_RAW_compressed/2018-12-22/SPHER.2018-12-23T02_25_30.081.fits.Z'
filename_out = 'E:/ESO/Data/SPHERE/SPARTA_RAW/2018-12-22/SPHER.2018-12-23T02_25_30.081.fits'




#%%

from astropy.io import fits

# read the fits file
hdul = fits.open(filename_out)



#%%
path_output = Path('E:/ESO/Data/SPHERE/DTTS_2/2018-12-22')
compressed_files = Path('E:/ESO/Data/SPHERE/SPARTA_RAW/2018-12-22')
plot = True
verbose = True

path_input = compressed_files
compressed_files = [os.path.join(path_input,f) for f in os.listdir(compressed_files)]

plot_sparta_data_2(path_output, compressed_files, plot=True, verbose=True)


#%%
# filename_in  = 'E:/ESO/Data/SPHERE/SPARTA_RAW_compressed/2018-12-22/SPHER.2018-12-23T02_25_30.081.fits.Z'
# filename_out = 'E:/ESO/Data/SPHERE/SPARTA_RAW_compressed/SPHER.2018-12-23T02_25_30.081.fits'

# from unlzw3 import unlzw
# with open(filename_in, 'rb') as fh:
#     hdr = fits.HDUList.fromstring(unlzw(fh.read()))

# # writing hdr to a file
# # hdr.writeto(filename_in.rsplit(".", 1)[0], overwrite=True)
# hdr.writeto(filename_out, overwrite=True)

# path_output = Path('E:/ESO/Data/SPHERE/DTTS_2/2018-12-22')
# files = Path('E:/ESO/Data/SPHERE/SPARTA_RAW/2018-12-22')
# plot = True
# verbose = True

# path_input = files
# files = [os.path.join(path_input,f) for f in os.listdir(files)]

# plot_sparta_data_2(path_output, files, plot=True, verbose=True)
