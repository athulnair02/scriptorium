'''
Crop a region from a zarr dataset and save as a new dataset
'''

import logging
import os
import json

import zarr

from utils import create_zarr

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def main():
    # Read data to crop
    zarr_path = '/scratch2/athulnair/tk_FIBICSTEST.zarr'
    arr_path = 'volumes/raw_equalized_0.02'

    logger.info(f' reading {zarr_path}/{arr_path}')
    data = zarr.open(os.path.join(zarr_path, arr_path), 'r')
    resolution = data.attrs['resolution']

    # Crop data z1, y1, x1, z2, y2, x2
    crop_s = (660, 130, 2120)
    crop_e = (1024, 494, 2484)

    data = data[crop_s[0]:crop_e[0], crop_s[1]:crop_e[1], crop_s[2]:crop_e[2]]

    logger.info(f' cropped to shape {data.shape}')

    # Create zarr amd save data
    arr_out_path = f'volumes/crops/raw_eq_0.02'
    create_zarr(zarr_path, arr_out_path, data=data, offset=crop_s, resolution=resolution, chunk_size=128, dtype=data.dtype)

main()