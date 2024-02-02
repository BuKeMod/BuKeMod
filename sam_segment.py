
from samgeo import SamGeo
import numpy
from filefolder_manage import create_folder,folder_to_zip
import os

import geopandas as gpd
import shapely
import rasterio
def segment(image, output_path='segment_output', filename=None,batch=False,model_type='vit_h'):

    sam_kwargs= get_samkwargs()


    sam = SamGeo(
        model_type=model_type,
        # checkpoint="/content/drive/MyDrive/model/epoch-000090-f10.98-ckpt.pth",
        sam_kwargs=sam_kwargs,
    )
        

    filename = create_folder_from_imageformat(image,output_path,filename)


    mask = f"{output_path}/{filename}/segment_mask.tif"
    shapefile = f'{output_path}/{filename}/segment_shapefile.shp'

    sam.generate(
        image, mask, batch=eval(batch), foreground=True, erosion_kernel=(3, 3), mask_multiplier=255,
        # sam_kwargs=sam_kwargs
    )


    sam.raster_to_vector(mask,shapefile)
   

    # sam.show_masks(cmap="binary_r")

def segment_drone(image_path,image_resize, output_path='segment_output', filename=None,batch=False,model_type='vit_h',imgtype='None'):


    sam_kwargs = {
        "points_per_side": 32,                      # points_per_side: Optional[int] = 32,
        "points_per_batch": 64,                     # points_per_batch: int = 64,
        "pred_iou_thresh": 0.88,                    # pred_iou_thresh: float = 0.88,
        "stability_score_thresh": 0.95,             # stability_score_thresh: float = 0.95,
        "stability_score_offset": 1,                # stability_score_offset: float = 1.0,
        "box_nms_thresh": 0.7,                      # box_nms_thresh: float = 0.7,
        "crop_n_layers": 0,                         # crop_n_layers: int = 0,
        "crop_nms_thresh": 0.7,                     # crop_nms_thresh: float = 0.7,
        "crop_overlap_ratio": 512 / 1500,           # crop_overlap_ratio: float = 512 / 1500,
        "crop_n_points_downscale_factor": 1,        # crop_n_points_downscale_factor: int = 1,
        "point_grids": None,                        # point_grids: Optional[List[np.ndarray]] = None,
        "min_mask_region_area": 0,                  # min_mask_region_area: int = 0,
        "output_mode":"binary_mask"                 # output_mode: str = "binary_mask",
        }

    sam = SamGeo(
        model_type=model_type,
        # checkpoint="/content/drive/MyDrive/model/epoch-000090-f10.98-ckpt.pth",
        sam_kwargs=None,
    )
        

    filename = create_folder_from_imageformat(image_path,output_path,filename)


    mask = f"{output_path}/{filename}/segment_mask.tif"
    shapefile = f'{output_path}/{filename}/segment_shapefile.shp'

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

def get_samkwargs():
    import os, ast
    from dotenv import load_dotenv, dotenv_values
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'env.configs')
    load_dotenv(env_path)

    configs = os.environ
    if ast.literal_eval(configs["SAM_KWARGS"]) == True :
        kwargs = {
            'points_per_side' : int(configs["POINTS_PER_SIDE"]),
            'points_per_batch': int(os.getenv("POINTS_PER_BATCH")),
            'pred_iou_thresh': float(os.getenv("PRED_IOU_THRESH")),
            'stability_score_thresh': float(os.getenv("STABILITY_SCORE_THRESH")),
            'stability_score_offset': float(os.getenv("STABILITY_SCORE_OFFSET")),
            'box_nms_thresh': float(os.getenv("BOX_NMS_THRESH")),
            'crop_n_layers': int(os.getenv("CROP_N_LAYERS")),
            'crop_nms_thresh': float(os.getenv("CROP_NMS_THRESH")),
            'crop_overlap_ratio': float(os.getenv("CROP_OVERLAP_RATIO")),
            'crop_n_points_downscale_factor': int(os.getenv("CROP_N_POINTS_DOWNSCALE_FACTOR")),
            'min_mask_region_area': int(os.getenv("MIN_MASK_REGION_AREA")),
            'output_mode': os.getenv("OUTPUT_MODE")
                    }
        return kwargs
    else:
        return None

if __name__ == '__main__':
    get_samkwargs()