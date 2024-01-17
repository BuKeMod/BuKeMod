from image_filter import imagefilter
from filefolder_manage import setimagepath
from sam_segment import segment

from argumentParser import create_parser    

def multi_image(image_path,output_path='vector_output',brightscale=1,batch=False):

  

    image_paths = setimagepath(image_path)
    image_filters = [imagefilter(image_path) for image_path in image_paths]
 
    # ให้ ImageFilter ปรับภาพแต่ละรูป
    for image_filter in image_filters:
        folder_infilename = image_filter.get_filename()


        image_filter.bright_image(brightscale)
        image = image_filter.get_image_temp(output_path=output_path, quality=100)

  
     
        segment(image,output_path,batch)
       
if __name__ == '__main__':
    args = create_parser()
    multi_image(image_path=args.image_path,brightscale=1.2,batch=args.batch)