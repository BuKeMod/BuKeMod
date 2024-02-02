
from samgeo import SamGeo
import numpy
from filefolder_manage import create_folder,folder_to_zip
import os

import geopandas as gpd
import shapely
import rasterio

from env_data_ import get_checkpoint,get_samkwargs
def segment(image, output_path='segment_output', filename=None,batch=False,model_type='vit_h'):

   


    sam = SamGeo(
        model_type=model_type,
        checkpoint=get_checkpoint(),
        sam_kwargs=get_samkwargs(),
    )
        

    filename = create_folder_from_imageformat(image,output_path,filename)


    mask = f"{output_path}/{filename}/{filename}_segment_mask.tif"
    shapefile = f'{output_path}/{filename}/{filename}_segment_shapefile.shp'

   
    sam.generate(
        image, mask, batch=eval(batch), foreground=True, erosion_kernel=(3, 3), mask_multiplier=255,
        # sam_kwargs=sam_kwargs
    )


    sam.raster_to_vector(mask,shapefile)
   

    # sam.show_masks(cmap="binary_r")

def segment_drone(image_path,image_resize, output_path='segment_output', filename=None,batch=False,model_type='vit_h',imgtype='None'):


    sam = SamGeo(
        model_type=model_type,
        checkpoint=get_checkpoint(),
        sam_kwargs=get_samkwargs(),
    )
        

    filename = create_folder_from_imageformat(image_path,output_path,filename)


    mask = f"{output_path}/{filename}/{filename}_segment_mask.tif"
    shapefile = f'{output_path}/{filename}/{filename}_segment_shapefile.shp'

    sam.generate(
        image_resize, mask, batch=eval(batch), foreground=True, erosion_kernel=(3, 3), mask_multiplier=255,
        # sam_kwargs=sam_kwargs
    )


    from resize_image import restore_original_size
    imagepath_restore = restore_original_size(image_path, mask)

    from image_to_image import image_to_tif
    from filefolder_manage import getfilename,getdirpath

 

    image_tiff = image_to_tif(image=imagepath_restore, source=image_path, output_path=getdirpath(imagepath_restore), output_name=getfilename(imagepath_restore))


    raster_to_vector(image_tiff,shapefile,area_threshold=999)
    
   

    # sam.show_masks(cmap="binary_r")






def create_folder_from_imageformat(image,output_path,filename):
    if type(image) == numpy.ndarray and filename != None:
        create_folder(f'{output_path}/{filename}')

    elif filename == None:

        directory, filename = os.path.split(image)
        filename = os.path.splitext(filename)[0]

        create_folder(f'{output_path}/{filename}')
    else:
        filename = "segment_mask"
    
    return filename




def raster_to_vector(source, output, simplify_tolerance=None, dst_crs=None, area_threshold=1000, **kwargs):

    from rasterio import features


    with rasterio.open(source) as src:
        band = src.read()

        mask = band != 0
        shapes = features.shapes(band, mask=mask, transform=src.transform)

    fc = [
        {"geometry": shapely.geometry.shape(shape), "properties": {"value": value}}
        for shape, value in shapes
    ]

    if simplify_tolerance is not None:
        for i in fc:
            i["geometry"] = i["geometry"].simplify(tolerance=simplify_tolerance)

    gdf = gpd.GeoDataFrame.from_features(fc)
    if src.crs is not None:
        gdf.set_crs(crs=src.crs, inplace=True)

    if dst_crs is not None:
        gdf = gdf.to_crs(dst_crs)

    if area_threshold is not None:
        # Create a new column 'area' to store the area of each geometry
        gdf['area'] = gdf['geometry'].area

        # Define a condition to filter out small polygons
        condition = gdf['area'] > area_threshold

        # Filter the GeoDataFrame based on the condition
        gdf = gdf[condition]

        # Drop the 'area' column as it is no longer needed
        gdf = gdf.drop(columns=['area'])

    gdf.to_file(output, **kwargs)


