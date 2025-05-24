import logging
import os
import zarr
import json
from numcodecs import Zlib

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def create_zarr(zarr_path,
                arr_zarr,
                data=None,
                shape=None,
                chunk_size=256,
                offset=[0, 0, 0],
                resolution=[5.24, 4, 4],
                dtype='<u4',
                safe=True):
    """
    Create an empty zarr container containing an empty array
    of specified shape and chunk size. If data is provided, uses
    data to fill in array.
    """
    root = zarr.group(store=zarr_path, overwrite=False)
    groups_path, dataset_name = os.path.split(arr_zarr)
    groups = groups_path.split('/')

    current_path = zarr_path
    for level, next_group in enumerate(groups):
        current_path = os.path.join(current_path, next_group)
        try:
            group = zarr.open_group(store=current_path, mode='r')
        except zarr.errors.GroupNotFoundError:
            logger.info(f' creating group {next_group}. Will override all existing datasets inside')
            input("Enter to continue:")        
            group = zarr.open_group(store=current_path, mode='w')
    group._read_only = False
    logger.info(f' creating {dataset_name}, with chunksize {chunk_size}')

    if safe:
        input("Enter to continue: ")

    if data is not None and not shape:    
        dataset = group.create_dataset(dataset_name,
                                       data=data,
                                       overwrite=True,
                                       compressor=Zlib(level=3),
                                       chunks=(chunk_size, chunk_size, chunk_size),
                                       dtype=dtype)
    elif not data and shape:
         dataset = group.create_dataset(dataset_name,
                                        overwrite=True,
                                        shape=shape,
                                        compressor=Zlib(level=3),
                                        chunks=(chunk_size, chunk_size, chunk_size),
                                        dtype=dtype)
    else:
         raise Exception('Cannot pass data and shape together. Pass in one or the other.')
         
    offset = tuple(o * r for o, r in zip(offset, resolution))
    dataset.attrs['offset'] = offset
    dataset.attrs['resolution'] = resolution

    zattrs = {'offset' : offset, 'resolution' : resolution}

    with open(os.path.join(zarr_path, arr_zarr, '.zattrs'), 'w') as out:
            json.dump(zattrs, out, indent=4)

    dataset_path = os.path.join(zarr_path, arr_zarr)
    logger.debug(f' dataset_path {dataset_path}')

    return dataset_path
