from image_filter import imagefilter
from filefolder_manage import setimagepath, folder_to_zip, getfilename
from geotiff_utility import processimagetif
from sam_segment import segment, segment_drone
from sam_object_detection import detection

from resize_image import resize_image_scale


from env_data import env_data
configs = env_data()


def filter_image(image_path):
    filter_use = False
    brightscale = configs.get_brightscale()
    quality = configs.get_quality()
    blur_image = configs.get_blur_image()
    hsv_image = configs.get_hsv_image()
    gray_image = configs.get_gray_image()
    output_path =  configs.get_output_path()

    image = imagefilter(image_path)
    if  brightscale != False:
        print('brightscale')
        image.bright_image(brightscale)
        filter_use = True
    if blur_image != False:
        print('blur_image')
        image.blur_image()
        filter_use = True
    if hsv_image != False:
        print('hsv_image')
        image.hsv_image()
        filter_use = True
    if gray_image != False:
        print('gray_image')
        image.gray_image()
        filter_use = True
    if filter_use:
        print('filter_use')
        return image.get_image_temp(
            output_path=output_path, quality=quality)
    else:
        print('No filter')
        return image_path


def image_segment(image_path, output_path='segment_output'):

    image_paths = setimagepath(image_path)

    if isinstance(image_paths, list):
        print("---multi image segment process---")

        image_filters = [filter_image(image_path)
                         for image_path in image_paths]
        # ให้ ImageFilter ปรับภาพแต่ละรูป
        for image_filter in image_filters:

            segment(image_filter, output_path
                     )

            print(f"*{getfilename(image_filter)} segment success")

    else:
        print("single image segment process")

        image = filter_image(image_path)

        segment(image, output_path)

        print(f"{getfilename(image)} segment success")
    folder_to_zip(f'{output_path}', f'{getfilename(output_path)}')


def image_detection(image_path, output_path='detection_output', text_prompt='', box_threshold=0.2, text_threshold=0.2):

    image_paths = setimagepath(image_path)

    if isinstance(image_paths, list):
        print("---multi image detection process---")

        image_filters = [filter_image(image_path)
                         for image_path in image_paths]

        # ให้ ImageFilter ปรับภาพแต่ละรูป
        for image_filter in image_filters:

            detection(image_filter, output_path, text_prompt,
                      box_threshold, text_threshold)

            print(f"{getfilename(image_filter)}  detection success")
    else:
        print("---single image detection process---")

        image = filter_image(image_path)

        detection(image, output_path, text_prompt,
                  box_threshold, text_threshold)

        print(f"{getfilename(image)}  detection success")

    folder_to_zip(f'{output_path}', f'{getfilename(output_path)}')


def image_segment_satellite_img(image_path, output_path='segment_output'):
    image_paths = setimagepath(image_path)

    if isinstance(image_paths, list):
        print("---multi image_segment_satellite process---")

        image_filters = [filter_image(image_path)
                         for image_path in image_paths]

        # ให้ ImageFilter ปรับภาพแต่ละรูป
        for image_filter in image_filters:
            image = processimagetif(image_filter)
            imgpath = image.get_image_withCoordinates(output_path)

            segment(imgpath, output_path)

            print(f"{getfilename(image)} satellite segment success")
    else:
        image = processimagetif(image_path)
        imgpath = image.get_image_withCoordinates(output_path)

        image = filter_image(imgpath)

        segment(image, output_path)
        print(f"{getfilename(image)} satellite segment success")

    folder_to_zip(f'{output_path}', f'{getfilename(output_path)}')


def image_segment_drone(image_path, output_path='segment_output'):

    image_paths = setimagepath(image_path)
    if isinstance(image_paths, list):
        print("---multi image segment drone process---")

        for image_filter in image_paths:

            image = filter_image(image_filter)
            image_resize = resize_image_scale(image, output_path)
            
            segment_drone(image_filter, image_resize, output_path
                          )
            print(f"{getfilename(image)} drone segment success")
    else:
        image = filter_image(image_path)
        image_resize = resize_image_scale(image, output_path)
        segment_drone(image_path, image_resize, output_path
                       )
        print(f"{getfilename(image)} drone segment success")
    folder_to_zip(f'{output_path}', f'{getfilename(output_path)}')


if __name__ == '__main__':
    segment_type = configs.get_segment_type()
    image_path = configs.get_image_path()
    output_path = configs.get_output_path()

    text_prompt = configs.get_text_prompt()
    box_threshold = configs.get_box_threshold()
    text_threshold = configs.get_text_threshold()

    if segment_type == '1':
        image_segment(image_path=image_path, output_path=output_path)
    elif segment_type == '2':
        image_detection(image_path=image_path, output_path=output_path, text_prompt=text_prompt,
                        box_threshold=box_threshold, text_threshold=text_threshold)
    elif segment_type == '3':
        image_segment_satellite_img(image_path=image_path, output_path=output_path)
    elif segment_type == '4':
        image_segment_drone(image_path=image_path, output_path=output_path)
    else:
        print('request SEGMENT_TYPE')
# main.py
