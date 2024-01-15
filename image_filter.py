import cv2
import numpy as np
import os
from filefloder_manage import create_floder, delete_floder, floder_to_zip
from image_to_image import image_to_tif

# from tiff import convert_png_to_tiff

# # อ่านไฟล์ TIFF
# img = './tiff_img/img/Image.tif'
# image = cv2.imread(img, cv2.IMREAD_UNCHANGED)
#
# # ตรวจสอบว่าการอ่านไฟล์ได้สำเร็จหรือไม่
# if image is None:
#     print("Failed to read the TIFF file.")
# else:
#     # แปลงประเภทข้อมูลของภาพเป็น CV_64F
#     image_float = image.astype(np.float64)
#
#     # ทำให้ภาพสว่างขึ้น โดยการคูณทุกพิกเซลด้วยค่า scale
#     scale = 1.5
#     brightened_image = np.clip(image_float * scale, 0, 255).astype(np.uint8)
#
#     # แสดงภาพเเทนภาพที่ถูกเพิ่มความสว่าง
#     cv2.imshow('im', brightened_image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#     if brightened_image.dtype == np.float64:
#         brightened_image = (brightened_image * 255).astype(np.uint8)
#     output_path = './tiff_img/img/brightened_imagePNG.png'
#     cv2.imwrite(output_path, brightened_image)
#
#     convert_png_to_tiff(input_png='./tiff_img/img/brightened_imagePNG.png',
#                         output_tiff='./tiff_img/img/brightened_imageTIF.tif',
#                         reference_tiff=img)
#


class imagefilter:
    def __init__(self, file_path):
        self.file_path = file_path
        self.directory, self.filename = os.path.split(file_path)
        self.image = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)

    def get_directory(self):
        return self.directory

    def get_filename(self):
        return self.filename

    def get_image(self):
        return self.image

    def get_num_bands(self):
        num_bands = self.image.shape[2]
        print(f'The image has {num_bands} bands.')
        return num_bands

    def bright_image(self, scale=1):
        image_float = self.image.astype(np.float64)
        self.image = np.clip(image_float * scale, 0, 255).astype(np.uint8)

    def imageshow(self):
        cv2.imshow(f'{self.filename}', self.image)
        cv2.waitKey(6000)
        cv2.destroyAllWindows()

    def _encode_image(self, image, quality=100):
        return cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, quality])[1]

    def _decode_image(self, encoded_image):
        return cv2.imdecode(encoded_image, cv2.IMREAD_UNCHANGED)

    def save_image(self, output_path='filteroutput_jpg', quality=100):
        create_floder(output_path)
        params = [cv2.IMWRITE_JPEG_QUALITY, quality]
        cv2.imwrite(f'{output_path}/{self.filename}.jpg', self.image, params)

    def save_image_tif(self, output_path='filteroutput_tif', quality=100):
        create_floder(output_path)
        jpeg_image = self._encode_image(self.image, quality)
        decoded_image = self._decode_image(jpeg_image)
        image_to_tif(image=decoded_image, source=self.file_path,
                     output_path=output_path, output_name=self.filename)

    def get_image(self, quality=100):
        jpeg_image = self._encode_image(self.image, quality)
        decoded_image = self._decode_image(jpeg_image)
        return decoded_image

    def get_image_temp(self, output_path='temp', quality=100):

        create_floder(output_path)
        jpeg_image = self._encode_image(self.image, quality)
        decoded_image = self._decode_image(jpeg_image)
        imagepath_temp = image_to_tif(image=decoded_image, source=self.file_path,
                                      output_path=output_path, output_name=self.filename)
        return imagepath_temp
