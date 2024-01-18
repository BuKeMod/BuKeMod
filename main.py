from image_filter import imagefilter
from filefolder_manage import setimagepath
from sam_segment import segment
from sam_object_detection import detection
from argumentParser import create_parser


def image_segment(image_path, output_path='segment_output', brightscale=1, batch=False, model_type='vit_h'):

    image_paths = setimagepath(image_path)

    if isinstance(image_paths, list):
        print("multi image segment process")

        image_filters = [imagefilter(image_path) for image_path in image_paths]
        # ให้ ImageFilter ปรับภาพแต่ละรูป
        for image_filter in image_filters:

            image_filter.bright_image(brightscale)
            image = image_filter.get_image_temp(
                output_path=output_path, quality=100)

            segment(image, output_path, batch=batch, model_type=model_type)
            print("multi image segment success")

    else:
        print("single image segment process")

        image_filter = imagefilter(image_path)
        image_filter.bright_image(brightscale)
        image = image_filter.get_image_temp(
            output_path=output_path, quality=100)

        segment(image, output_path, batch=batch, model_type=model_type)
        print("single image segment success")


def image_detection(image_path, output_path='detection_output', brightscale=1, text_prompt='', box_threshold=0.2, text_threshold=0.2):

    image_paths = setimagepath(image_path)

    if isinstance(image_paths, list):
        print("multi image detection process")

        image_filters = [imagefilter(image_path) for image_path in image_paths]

        # ให้ ImageFilter ปรับภาพแต่ละรูป
        for image_filter in image_filters:

            image_filter.bright_image(brightscale)
            image = image_filter.get_image_temp(
                output_path=output_path, quality=100)

            detection(image, output_path, text_prompt,
                    box_threshold, text_threshold)
            print("multi image detection success")
    else:
        print("single image detection process")

        image_filter = imagefilter(image_path)
        image_filter.bright_image(brightscale)
        image = image_filter.get_image_temp(
            output_path=output_path, quality=100)

        detection(image, output_path, text_prompt,
                box_threshold, text_threshold)
        print("single image detection success")




if __name__ == '__main__':
    args = create_parser()
    model_type = args.model_type
    text_prompt = 'house'
    #image_segment(image_path=args.image_path,brightscale=1.2,batch=args.batch,model_type=model_type)
    image_detection(image_path=args.image_path, text_prompt=text_prompt,
                           brightscale=1.2, box_threshold=0.2, text_threshold=0.2)


# main.py
