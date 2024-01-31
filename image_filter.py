import cv2
import numpy as np
import os
from filefolder_manage import create_folder
from image_to_image import image_to_tif


class imagefilter:
    def __init__(self, file_path):
        self.file_path = file_path
        self.directory, self.filename = os.path.split(file_path)
        self.filenamesplit =  os.path.splitext(self.filename)[0]
        
        self.image = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
    def get_filepath(self):
        return self.file_path
    def get_directory(self):
        return self.directory

    def get_filename(self):
        return self.filename
    
    def get_num_bands(self):
        num_bands = self.image.shape[2]
        print(f'The image has {num_bands} bands.')
        return num_bands

    def bright_image(self, scale=1):
        print(f'image bright scale ',{scale})
        # image_float = self.image.astype(np.float64)
        # self.image = np.clip(image_float * scale, 0, 255).astype(np.uint8)
        self.image = np.clip(self.image * scale, 0, 255)


    def blur_image(self, scalepixelx=3, scalepixely=3,deviation=1):
        self.image = cv2.GaussianBlur(self.image, (scalepixelx,scalepixely ), deviation )

    def hsv_image(self):
        self.image = cv2.cvtColor(self.image, cv2.COLOR_RGB2HSV)

    def gray_image(self):
        self.image = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)

    def rgb_image(self):
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)


    def imageshow(self):
        cv2.imshow(f'{self.filename}', self.image)
        cv2.waitKey(6000)
        cv2.destroyAllWindows()



    def _encode_image(self, image, quality=100):
        return cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, quality])[1]

    def _decode_image(self, encoded_image):
        return cv2.imdecode(encoded_image, cv2.IMREAD_UNCHANGED)

    def save_image(self, output_path='filteroutput_jpg', quality=100,extension='jpg'):
        create_folder(output_path)
        params = [cv2.IMWRITE_JPEG_QUALITY, quality]
        cv2.imwrite(f'{output_path}/{self.filenamesplit}.{extension}', self.image, params)

    def save_image_tif(self, output_path='filteroutput_tif', quality=100):
        create_folder(output_path)
        jpeg_image = self._encode_image(self.image, quality)
        decoded_image = self._decode_image(jpeg_image)
        image_to_tif(image=decoded_image, source=self.file_path,
                     output_path=output_path, output_name=self.filenamesplit)

    def get_image(self, quality=100):
        jpeg_image = self._encode_image(self.image, quality)
        decoded_image = self._decode_image(jpeg_image)
        return decoded_image

    def get_image_temp(self, output_path='temp', quality=100):

        create_folder(output_path)
        jpeg_image = self._encode_image(self.image, quality)
        decoded_image = self._decode_image(jpeg_image)
        imagepath_temp = image_to_tif(image=decoded_image, source=self.file_path,
                                      output_path=output_path, output_name=self.filenamesplit)
        return imagepath_temp





