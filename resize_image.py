from PIL import Image
#pillow 9.5.0
def resize_image(input_path, output_path, scale_factor):
    # Open the image
    with Image.open(input_path) as img:
        # Get the original size
        original_width, original_height = img.size

        # Calculate the new size
        target_width = int(original_width * scale_factor)
        target_height = int(original_height * scale_factor)

        # Resize the image
        img_resized = img.resize((target_width, target_height), Image.ANTIALIAS)

        # Save the resized image
        img_resized.save(output_path)


def resize_image_input(input_path, output_path, width, height):
    # Open the image
    with Image.open(input_path) as img:
        # Get the original size
        original_width, original_height = img.size

        # Resize the image
        img_resized = img.resize((width, height), Image.ANTIALIAS)

        # Save the resized image
        img_resized.save(output_path)

if __name__ == '__main__':
    # # Example usage
    # input_path_original = "Task.tif"
    # output_path_resized = "resized_imageTIF.tif"


    input_path_original = "segment_mask.tif"
    output_path_resized = "over_imageTIF.tif"

    scale_factor = 10  # Adjust this value based on how much you want to resize the image

    # resize_image(input_path_original, output_path_resized, scale_factor)

    resize_image_input(input_path_original, output_path_resized, 9206, 10236)