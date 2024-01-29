
from samgeo import SamGeo
import numpy
from filefolder_manage import create_folder,folder_to_zip
import os

def segment(image, output_path='segment_output', filename=None,batch=False,model_type='vit_h'):


    sam_kwargs = {
        "points_per_side": 32,                  # points_per_side: Optional[int] = 32,
                                                # points_per_batch: int = 64,
        "pred_iou_thresh": 0.88, 
        "stability_score_thresh": 0.95,
        "crop_n_layers": 1,
        "crop_n_points_downscale_factor": 1,
        "min_mask_region_area": 100,
                   
                                                # pred_iou_thresh: float = 0.88,
                                                # stability_score_thresh: float = 0.95,
                                                # stability_score_offset: float = 1.0,
                                                # box_nms_thresh: float = 0.7,
                                                # crop_n_layers: int = 0,
                                                # crop_nms_thresh: float = 0.7,
                                                # crop_overlap_ratio: float = 512 / 1500,
                                                # crop_n_points_downscale_factor: int = 1,
                                                # point_grids: Optional[List[np.ndarray]] = None,
                                                # min_mask_region_area: int = 0,
                                                # output_mode: str = "binary_mask",
        }

    sam = SamGeo(
        model_type=model_type,
        # checkpoint="/content/drive/MyDrive/model/epoch-000090-f10.98-ckpt.pth",
        sam_kwargs=None,
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
        "points_per_side": 32,                  # points_per_side: Optional[int] = 32,
                                                # points_per_batch: int = 64,
        "pred_iou_thresh": 0.88, 
        "stability_score_thresh": 0.95,
        "crop_n_layers": 1,
        "crop_n_points_downscale_factor": 1,
        "min_mask_region_area": 100,
                   
                                                # pred_iou_thresh: float = 0.88,
                                                # stability_score_thresh: float = 0.95,
                                                # stability_score_offset: float = 1.0,
                                                # box_nms_thresh: float = 0.7,
                                                # crop_n_layers: int = 0,
                                                # crop_nms_thresh: float = 0.7,
                                                # crop_overlap_ratio: float = 512 / 1500,
                                                # crop_n_points_downscale_factor: int = 1,
                                                # point_grids: Optional[List[np.ndarray]] = None,
                                                # min_mask_region_area: int = 0,
                                                # output_mode: str = "binary_mask",
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

 

    image_tiff = image_to_tif(image=imagepath_restore, source=image_path, output_path=getdirpath(imagepath_restore), output_name=getfilename(imagepath_restore)


    sam.raster_to_vector(image_tiff,shapefile)
    
   

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