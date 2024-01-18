from samgeo.text_sam import LangSAM
import numpy
from filefolder_manage import create_folder,folder_to_zip
import os



def detection(image,output_path='detection_output',text_prompt='fram',box_threshold=0.2, text_threshold=0.2):

    sam = LangSAM()


    filename = create_folder_from_imageformat(image,output_path)


    sam.predict(image, text_prompt, box_threshold, text_threshold)



    sam.show_anns(
        cmap='Accent_r',
        box_color='red',
        title=f'Automatic Segmentation of {text_prompt}',
        blend=False,
        output=f'{output_path}/{filename}/{filename}_detection_boxs.tif'
    )

    sam.raster_to_vector(f'{output_path}/{filename}/{filename}_detection_boxs.tif', f'{output_path}/{filename}/{filename}_detection_shapefile.shp')
    
    folder_to_zip(f'{output_path}','detection_output')




def create_folder_from_imageformat(image,output_path,filename=None):
    if type(image) == numpy.ndarray and filename != None:
        create_folder(f'{output_path}/{filename}')

    elif filename == None:

        directory, filename = os.path.split(image)
        filename = os.path.splitext(filename)[0]

        create_folder(f'{output_path}/{filename}')
    else:
        filename = "segment_mask"
    
    return filename