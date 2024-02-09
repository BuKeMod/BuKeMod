import numpy
from filefolder_manage import create_folder,folder_to_zip
import os

import geopandas as gpd
import shapely
import rasterio


from env_data import env_data
envdata = env_data()
file_extension = envdata.get_output_extension()
area_threshold = envdata.get_min_polygon_area()
batch = envdata.get_batch()

def segment(image, output_path='segment_output', filename=None):
    print('segment')
   


    sam = create_sam(envdata.get_model())
        

    filename = create_folder_from_imageformat(image,output_path,filename)

    

    mask = f"{output_path}/{filename}/{filename}_segment_mask.tif"
    shapefile = f'{output_path}/{filename}/{filename}_segment_{file_extension}_file.{file_extension}'

   
    sam.generate(
        image, mask, batch=batch, foreground=True, erosion_kernel=(3, 3), mask_multiplier=255,
        # sam_kwargs=sam_kwargs
    )


    raster_to_vector(mask,shapefile,area_threshold)
   

    # sam.show_masks(cmap="binary_r")

def segment_drone(image_path,image_resize, output_path='segment_output', filename=None,imgtype='None'):
    print('segment_drone')

    sam = create_sam(envdata.get_model())
        

    filename = create_folder_from_imageformat(image_path,output_path,filename)


    mask = f"{output_path}/{filename}/{filename}_segment_mask.tif"
    shapefile = f'{output_path}/{filename}/{filename}_segment_{file_extension}_file.{file_extension}'

    sam.generate(
        image_resize, mask, batch=batch, foreground=True, erosion_kernel=(3, 3), mask_multiplier=255,
        # sam_kwargs=sam_kwargs
    )


    image_tiff = resizeimgae_check(image_path,image_resize,mask)

    raster_to_vector(image_tiff,shapefile,area_threshold)
    
   

    # sam.show_masks(cmap="binary_r")
def resizeimgae_check(image_path,image_resize,mask):    
    if image_path != image_resize:
        from resize_image import restore_original_size
        imagepath_restore = restore_original_size(image_path, mask)
        
        from image_to_image import image_to_tif
        from filefolder_manage import getfilename,getdirpath

        image_tiff = image_to_tif(image=imagepath_restore, source=image_path, output_path=getdirpath(imagepath_restore), output_name=getfilename(imagepath_restore))
        return image_tiff
    else:
        return mask
    



def create_sam(sam_type):
    if sam_type == 'sam':
        from samgeo import SamGeo
        sam = SamGeo(
            model_type=envdata.get_model_type(),
            checkpoint=envdata.get_checkpoint(),
            sam_kwargs=envdata.get_samkwargs(),
        )
        return sam
    elif sam_type == 'hqsam':
        from samgeo.hq_sam import SamGeo
        sam = SamGeo(
            model_type=envdata.get_model_type(),
            checkpoint=envdata.get_checkpoint(),
            sam_kwargs=envdata.get_samkwargs(),
        )
        return sam
    else:
        print('sam_type not found or not support,please enter sam or hqsam.')

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




def raster_to_vector(source, output,area_threshold=100, simplify_tolerance=None, dst_crs=None,  **kwargs):

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


