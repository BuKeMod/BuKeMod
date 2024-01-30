from image_filter import imagefilter
from filefolder_manage import setimagepath, folder_to_zip
from geotiff_utility import processimagetif
from sam_segment import segment ,segment_drone
from sam_object_detection import detection
from argumentParser import create_parser
from resize_image import resize_image_scale

def image_segment(image_path, output_path='segment_output', brightscale=1, batch=False, model_type='vit_h'):

    image_paths = setimagepath(image_path)

    if isinstance(image_paths, list):
        print("---multi image segment process---")

        image_filters = [imagefilter(image_path) for image_path in image_paths]
        # ให้ ImageFilter ปรับภาพแต่ละรูป
        for image_filter in image_filters:

            if brightscale != 1:
                image_filter.bright_image(brightscale)
            image = image_filter.get_image_temp(
                output_path=output_path, quality=100)

            segment(image, output_path, batch=batch, model_type=model_type)

            filename = image_filter.get_filename()
            print(f"*{filename} segment success")

    else:
        print("single image segment process")

        image_filter = imagefilter(image_path)
        if brightscale != 1:
            image_filter.bright_image(brightscale)
        image = image_filter.get_image_temp(
            output_path=output_path, quality=100)

        segment(image, output_path, batch=batch, model_type=model_type)

        filename = image_filter.get_filename()
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
                image_resize = resize_image_scale(image)

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
            image_resize = resize_image_scale(image)

            segment_drone(image_path, image_resize, output_path, batch=batch, model_type=model_type)
        else:
            image_resize = resize_image_scale(image_path, output_path)
            segment_drone(image_path, image_resize, output_path, batch=batch, model_type=model_type)

    folder_to_zip(f'{output_path}', 'segment_output')


if __name__ == '__main__':
    args = create_parser()
    brightscale = args.bright
    model_type = args.model_type
    text_prompt = 'house'

    # image_segment(image_path=args.image_path, brightscale=brightscale,
    #               batch=args.batch, model_type=model_type)
    #
    # image_detection(image_path=args.image_path, text_prompt=text_prompt,
    #                 brightscale=brightscale, box_threshold=0.2, text_threshold=0.2)

    # image_segment_satellite_img(image_path=args.image_path,
    #               batch=args.batch, model_type=model_type)

    image_segment_drone(image_path=args.image_path,brightscale=brightscale,
                  batch=args.batch, model_type=model_type)
# main.py
