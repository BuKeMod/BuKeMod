import cv2
import rasterio
import numpy as np

def image_to_tif(
    image, source,output_path,output_name, dtype=None, compress="deflate"
):

    try:
        image = cv2.imread(image)
    except Exception as e: print('image_to_tif imread ',e)

    # with rasterio.open(image, 'r') as src:
    #     # อ่านข้อมูล
    #     array = src.read()

    with rasterio.open(source) as src:
        crs = src.crs
        transform = src.transform
        if compress is None:
            compress = src.compression

        # Determine the minimum and maximum values in the array

    min_value = np.min(image)
    max_value = np.max(image)

    if dtype is None:
            # Determine the best dtype for the array
        if min_value >= 0 and max_value <= 1:
                dtype = np.float32
        elif min_value >= 0 and max_value <= 255:
                dtype = np.uint8
        elif min_value >= -128 and max_value <= 127:
                dtype = np.int8
        elif min_value >= 0 and max_value <= 65535:
                dtype = np.uint16
        elif min_value >= -32768 and max_value <= 32767:
                dtype = np.int16
        else:
                dtype = np.float64

        # Convert the array to the best dtype
        data = image.astype(dtype)
        print('dtype',dtype)
        print('data.ndim',data.ndim)
        # Define the GeoTIFF metadata
        if data.ndim == 2:
            metadata = {
                "driver": "GTiff",
                "height": data.shape[0],
                "width": data.shape[1],
                "count": 1,
                "dtype": data.dtype,
                "crs": crs,
                "transform": transform,
            }
        elif data.ndim == 3:
            metadata = {
                "driver": "GTiff",
                "height": data.shape[0],
                "width": data.shape[1],
                "count": data.shape[2],
                "dtype": data.dtype,
                "crs": crs,
                "transform": transform,
            }
        # metadata = {
        #     "driver": "GTiff",
        #     "height": data.shape[1],
        #     "width": data.shape[2],
        #     "count": data.shape[0],
        #     "dtype": data.dtype,
        #     "crs": crs,
        #     "transform": transform,
        # }

        if compress is not None:
            metadata["compress"] = compress
        else:
            raise ValueError("Array must be 2D or 3D.")

        # Create a new GeoTIFF file and write the array to it
        with rasterio.open(f'{output_path}/{output_name}.tif', "w", **metadata) as dst:
            # dst.write(data)
            # if data.ndim == 2:
            #   dst.write(data, 1)
            # elif data.ndim == 3:
            #     for i in range(data.shape[0]): # Loop through the first dimension (bands)
            #         dst.write(data[i], i + 1)
            if image.ndim == 2:
                dst.write(image, 1)
            elif image.ndim == 3:
                for i in range(image.shape[2]):
                    dst.write(image[:, :, i], i + 1)

        return f'{output_name}.tif'


