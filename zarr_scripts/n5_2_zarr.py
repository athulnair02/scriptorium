'''
Converts a n5 data source into a zarr format
'''
import logging
import os

from fibsem_tools.io.core import read

import numpy as np
from utils import create_zarr

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Inputs into script
n5_path = '/scratch2/athulnair/jrc_hela-2.n5'
arr_n5 = 'eres_seg'
n5_arr_path = os.path.join(n5_path, arr_n5)

zarr_path = '/scratch2/athulnair/jrc_hela-2.zarr'
arr_zarr = 'volumes/janelia_predictions/eres_seg'
offset = [0, 0, 0]
resolution = [4, 4, 4]
chunk_size = 256

# Reading data
logger.info(f'  reading {n5_arr_path}')
data = read(n5_arr_path)
logger.info(f' final data {data}')

# Custom changes to the data to work with ASEM pipeline
# Fit fit data range into 0-255
factor = 16 # default 256
raw_8_bit = False
if raw_8_bit:
    data_int8 = (data/factor).astype('u1')
else:
    data_int8 = data

# Invert the image
invert = False
if invert and raw_8_bit:
    data_int8 = 255 - data_int8

# Flip the y axis
data_int8 = np.flip(np.array(data_int8), 1)

# Save the data as zarr at given destination
zarr_ds_path = create_zarr(zarr_path,
                           arr_zarr,
                           data=data_int8,
                           chunk_size=chunk_size,
                           offset=offset,
                           resolution=resolution,
                           dtype=data_int8.dtype)
