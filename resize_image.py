from PIL import Image
#pillow 9.5.0
import os
from filefolder_manage import getfilename, getdirpath,create_folder

def calculate_scale_factor(width, height, target_size):
    # Calculate the scale factor based on the smaller dimension
    min_dimension = min(width, height)
    scale_factor = target_size / min_dimension
    return scale_factor

def resize_image_scale(input_path,output_path):
    dir = getdirpath(input_path)
    filename = getfilename(input_path)

    create_folder(output_path)
    # Open the image
    image = Image.open(input_path)

    # Get the original size
    original_width, original_height = image.size

    # Set the target size
    target_size = 1440

    # Check if either dimension is smaller than 1000
    if original_width < target_size or original_height < target_size:
        # If either dimension is smaller than 1000, do not resize
        new_width, new_height = original_width, original_height
    else:
        # Calculate scale factor based on the smaller dimension
        scale_factor = calculate_scale_factor(original_width, original_height, target_size)

        # Calculate new dimensions
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)

    # Resize the image
    image = image.resize((new_width, new_height))
    save_path = f'{output_path}/{filename}/{filename}_resized.tif'
    # Save the resized image
    image.save(save_path)
    return save_path

def restore_original_size(original_path, resized_path):
    dir = getdirpath(resized_path)
    filename = getfilename(resized_path)
    # Open the original image
    original_image = Image.open(original_path)

    # Open the resized image
    resized_image = Image.open(resized_path)

    # Get the original size
    original_width, original_height = original_image.size

    # Resize the resized image to the original size
    restored_image = resized_image.resize((original_width, original_height), Image.ANTIALIAS)
    
    save_path = f'{dir}/{filename}_restore.png'
    # Save the restored image
    restored_image.save(save_path)
    return save_path

if __name__ == '__main__':
    # # Example usage
    # input_path_original = "Task.tif"
    # output_path_resized = "resized_imageTIF.tif"

    input_path_original = "segment_mask.tif"
    output_path_resized = "over_imageTIF.tif"

    scale_factor = 0.1  # Adjust this value based on how much you want to resize the image

    # resize_image_scale(input_path_original, output_path_resized, scale_factor)
