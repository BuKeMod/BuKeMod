import cv2
import numpy as np
import os
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
    def __init__(self,file_path):
        self.file_path = file_path
        self.directory, self.filename = os.path.split(file_path)
        self.image = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)

    def bright_image(self,scale=1):
        image_float = self.image.astype(np.float64)
        self.image = np.clip(image_float * scale, 0, 255).astype(np.uint8)

    def imageshow(self):
        cv2.imshow(f'{self.filename}',self.image)
        cv2.waitKey(6000)
        cv2.destroyAllWindows()


