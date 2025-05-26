'''
Given data and target resolution, downsamples the data and outputs it to a given location
'''

import logging
import os
import json

from scipy import ndimage

import dask
import dask.array as da

from dask.diagnostics import ProgressBar

from utils import create_zarr
import zarr
from numcodecs import Zlib

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# All inputs into script
zarr_path = '/nfs/tkhome/athulnair/incasem/data/jrc_hela-2/jrc_hela-2.zarr'
arr_zarr = 'volumes/labels/cop/cleaned_3400_4nm'
new_res = 8
arr_zarr_out = 'volumes/labels/cop/cleaned_1700_8nm'

zarr_arr_path = os.path.join(zarr_path, arr_zarr)
chunk_size = 256

# Read data in
logger.info(f' reading {zarr_arr_path}')
zarr_arr = zarr.open(zarr_arr_path)
data = da.from_array(zarr_arr,
                     chunks=(chunk_size, chunk_size, chunk_size),
                     asarray=True)
logger.info(f' initial data {data}')
shape = data.shape
logger.debug(f' subsection {data}')

# Zooming from original to new resolution
original_res = zarr_arr.attrs['resolution'][0]
ratio = original_res / new_res
data = ndimage.zoom(data, zoom=ratio)
data = da.from_array(data,
                     chunks=(chunk_size, chunk_size, chunk_size),
                     asarray=True)
logger.info(f' final data {data}')

# Create dataset and save data
offset = list(map(lambda x: round(x / new_res), zarr_arr.attrs['offset'])) # round to nearest new_res nm
resolution = (new_res, new_res, new_res)

logger.debug(f'old offset {zarr_arr.attrs["offset"]}')
logger.debug(f'offset {offset} resolution {resolution}')

chunk_size = 256

zarr_ds_path = create_zarr(zarr_path,
                           arr_zarr_out,
                           shape=data.shape,
                           chunk_size=chunk_size,
                           offset=offset,
                           resolution=resolution,
                           dtype=data.dtype)

logger.info(f'\n\n\t creating: {arr_zarr_out}\n')
stored = da.to_zarr(data,
            zarr_ds_path,
            component=None,
            overwrite=True,
            compute=False,
            return_stored=True,
            compressor=Zlib(level=3))

zattrs = {'offset' : tuple(o * r for o, r in zip(offset, resolution)), 'resolution' : resolution}

with open(os.path.join(zarr_ds_path, '.zattrs'), 'w') as out:
        json.dump(zattrs, out, indent=4)

with ProgressBar():
    dask.compute(stored)
