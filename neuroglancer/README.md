# Incasem Neuroglancer Quick View
A script that aids with quickly displaying different 3D images on neuroglancer without the need to manually type out the command each time. This is built for use while working with the [incasem](!https://github.com/kirchhausenlab/incasem) project as the folder structure in this script expects the same format from the input/output of data from that project. It can however be used independently with other zarrs if layers of interest are placed in the **Misc** section. 

## neuroglancer_script.py
TODO
## neuroglancer_input.txt
The text file with all the possible inputs needed for the local neuroglancer instance. To include a input, remove the `#` in the start of the line. To exclude a input parameter, add `#` at the start of the line. The input file includes:
### zarr files
The zarr file from which to read the layers from. ***Required**
### raw layers
The raw layers found in the `volumes` directory.
### labels
The label layers found in the `volumes/labels` directory.
### prediction id
The prediction id to read from the MongoDB database which will display the prediction from the correct subdirectory using this id and the pulled training id. Closely related to incasem, it produces layers in the following format: `volumes/predictions/train_<train_id>/predict_<pred_id>/segmentation`
### misc datasets
Any miscellaneous paths to zarr datasets wished to be displayed.
### bounds
Special zarr datasets with no actual data. These datasets only store metadata in `.zarray` and `.zattrs` that draw bounding boxes in neuroglancer at regions of interest. The format is `<prefix> <num_range>`. e.g `cop_ 13-15` will add 3 layers: `cop_13`, `cop_14`, and `cop_15`
