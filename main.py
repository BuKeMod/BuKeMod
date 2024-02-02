from image_filter import imagefilter
from filefolder_manage import setimagepath, folder_to_zip
from geotiff_utility import processimagetif
from sam_segment import segment ,segment_drone
from sam_object_detection import detection
from argumentParser import create_parser
from resize_image import resize_image_scale


import os
import ast
from dotenv import load_dotenv,dotenv_values

env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'env.configs')
load_dotenv(env_path)
configs = os.environ


def filter_image(image_path):
    filter_use = False
    brightscale = float(configs['BRIGHT'])
    quality = int(configs['QUALITY'])
    blur_image = ast.literal_eval(configs['BLUR_IMAGE'])
    hsv_image = ast.literal_eval(configs['HSV_IMAGE'])
    gray_image = ast.literal_eval(configs['GRAY_IMAGE'])
    output_path = configs['OUTPUT_PATH']
    
    image = imagefilter(image_path)
    if brightscale != 1:
        print('brightscale')
        image.bright_image(brightscale)
        filter_use = True
    if blur_image != 'False':
        print('blur_image')
        image.blur_image()
        filter_use = True
    if hsv_image != 'False':
        print('hsv_image')
        image.hsv_image()
        filter_use = True
    if gray_image != 'False':
        print('gray_image')
        image.gray_image()
        filter_use = True
    if filter_use:
        print('filter_use')
        return image.get_image_temp(
                output_path=output_path, quality=quality)
    else:
        return image_path

def image_segment(image_path, output_path='segment_output',batch=False, model_type='vit_h'):

    image_paths = setimagepath(image_path)

    if isinstance(image_paths, list):
        print("---multi image segment process---")

        image_filters = [filter_image(image_path) for image_path in image_paths]
        # ให้ ImageFilter ปรับภาพแต่ละรูป
        for image_filter in image_filters:

            segment(image_filter, output_path, batch=batch, model_type=model_type)

            filename = image_filter.get_filename()
            print(f"*{filename} segment success")

    else:
        print("single image segment process")

   
        image = filter_image(image_path)

        segment(image, output_path, batch=batch, model_type=model_type)

        filename = image.get_filename()
        print(f"{filename} segment success")
    folder_to_zip(f'{output_path}', 'segment_output')


def image_detection(image_path, output_path='detection_output', brightscale=1, text_prompt='', box_threshold=0.2, text_threshold=0.2):

    image_paths = setimagepath(image_path)

    if isinstance(image_paths, list):
        print("---multi image detection process---")

        image_filters = [imagefilter(image_path) for image_path in image_paths]

        # ให้ ImageFilter ปรับภาพแต่ละรูป
        for image_filter in image_filters:

            if brightscale != 1:
                image_filter.bright_image(brightscale)
            image = image_filter.get_image_temp(
                output_path=output_path, quality=100)

            detection(image, output_path, text_prompt,
                      box_threshold, text_threshold)

            filename = image_filter.get_filename()
            print(f"*{filename} detection success")
    else:
        print("---single image detection process---")

        image_filter = imagefilter(image_path)
        if brightscale != 1:
            image_filter.bright_image(brightscale)
        image = image_filter.get_image_temp(
            output_path=output_path, quality=100)

        detection(image, output_path, text_prompt,
                  box_threshold, text_threshold)

        filename = image_filter.get_filename()
        print(f"{filename} detection success")

    folder_to_zip(f'{output_path}', 'segment_output')



def image_segment_satellite_img(image_path,output_path='segment_output',brightscale=1,batch=False, model_type='vit_h'):
    image = processimagetif(image_path)
    imgpath = image.get_image_withCoordinates(output_path)
    image_filter = imagefilter(imgpath)
    if brightscale != 1:
        image_filter.bright_image(brightscale)
    image = image_filter.get_image_temp(
        output_path=output_path, quality=100)

    segment(image, output_path, batch=batch, model_type=model_type)

    folder_to_zip(f'{output_path}', 'segment_output')


def image_segment_drone(image_path,output_path='segment_output',brightscale=1,batch=False, model_type='vit_h'):

    image_paths = setimagepath(image_path)
    if isinstance(image_paths, list):
        print("---multi image segment drone process---")

        for image_filter in image_paths:

            image_path = image_filter

            if brightscale != 1:
                image_filter = imagefilter(image_path)
                image_filter.bright_image(brightscale)
                image = image_filter.get_image_temp(
                    output_path=output_path, quality=100)
                image_resize = resize_image_scale(image,output_path)
                segment_drone(image_path,image_resize, output_path, batch=batch, model_type=model_type)
            else:
                image_resize = resize_image_scale(image_path,output_path)
                segment_drone(image_path,image_resize, output_path, batch=batch, model_type=model_type)

    else:
        if brightscale != 1:
            image_filter = imagefilter(image_path)
            image_filter.bright_image(brightscale)
            image = image_filter.get_image_temp(
                output_path=output_path, quality=100)
            image_resize = resize_image_scale(image,output_path)

            segment_drone(image_path, image_resize, output_path, batch=batch, model_type=model_type)
        else:
            image_resize = resize_image_scale(image_path, output_path)
            segment_drone(image_path, image_resize, output_path, batch=batch, model_type=model_type)

    folder_to_zip(f'{output_path}', 'segment_output')


if __name__ == '__main__':

    image_path = configs['IMAGE_PATH']
    output_path = configs['OUTPUT_PATH']
    batch = configs['BATCH']
    model_type = configs['MODEL_TYPE']

    text_prompt = configs['TEXT_PROMPT']
    box_threshold = float(configs['BOX_THRESHOLD'])
    text_threshold = float(configs['TEXT_THRESHOLD'])



    if configs['SEGMENT_TYPE'] == '1':
        image_segment(image_path=image_path,output_path=output_path,batch=batch, model_type=model_type)
    elif configs['SEGMENT_TYPE'] == '2':
        image_detection(image_path=image_path,output_path=output_path, text_prompt=text_prompt,
                         box_threshold=box_threshold, text_threshold=text_threshold)
    elif configs['SEGMENT_TYPE'] == '3':
        image_segment_satellite_img(image_path=image_path,output_path=output_path,
                    batch=batch, model_type=model_type)
    elif configs['SEGMENT_TYPE'] == '4':
        image_segment_drone(image_path=image_path,output_path=output_path,
                      batch=batch, model_type=model_type)
    else:
        print('pls input SEGMENT_TYPE')
# main.py
