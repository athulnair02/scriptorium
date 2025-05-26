# Zarr Scripts
Useful scripts used to work with zarr datasets. Mainly used in conjunction with the [incasem](!https://github.com/kirchhausenlab/incasem) project.

## utils.py
Zarr utility function for creating a dataset. Future functions could be added here.

## zarr_crop.py
Crops a region out of a 3D array and produces a new dataset.

## n5_2_zarr.py
Converts an n5 dataset into a zarr dataset.

## downsample.py
Downsamples a zarr 3D dataset to a lower resolution. e.g 5x5x5nm<sup>3</sup> -> 8x8x8nm<sup>3</sup>. Uses SciPy ndimage library to downsample and dask to speed up the performance by parallelizing the work. Reads input dataset's resolution from the `.zattrs` file in the dataset.
