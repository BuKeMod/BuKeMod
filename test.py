# import os
# from dotenv import load_dotenv,dotenv_values
#
# configs = dotenv_values("env.configs")
#
# # print(configs)
# print(type(configs['BLUR_IMAGE']))
#
# if __name__ == '__main__':
#     print(configs['BATCH'])


import os
from dotenv import load_dotenv,dotenv_values



# ตั้งค่า path ที่อยู่ของไฟล์ .env
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'env.configs')

# ใช้คำสั่ง load_dotenv ดึงค่าจากไฟล์ .env
load_dotenv(env_path)

# ดึงค่าจากไฟล์ .env ด้วย os.getenv()
SEGMENT_TYPE = os.getenv('SEGMENT_TYPE')
IMAGE_PATH = os.getenv('IMAGE_PATH')
OUTPUT_PATH = os.getenv('OUTPUT_PATH')
MODEL_TYPE = os.getenv('MODEL_TYPE')
BATCH = os.getenv('BATCH')
TEXT_PROMPT = os.getenv('TEXT_PROMPT')
BOX_THRESHOLD = os.getenv('BOX_THRESHOLD')
TEXT_THRESHOLD = os.getenv('TEXT_THRESHOLD')
QUALITY = os.getenv('QUALITY')
BRIGHT = os.getenv('BRIGHT')
BLUR_IMAGE = os.getenv('BLUR_IMAGE')
HSV_IMAGE = os.getenv('HSV_IMAGE')
GRAY_IMAGE = os.getenv('GRAY_IMAGE')

# ดึงค่าทั้งหมดจากไฟล์ .env
env_data = os.environ

# ตรวจสอบค่าที่ถูกดึงมาทั้งหมด
print(env_data[''])
# ตรวจสอบค่าที่ถูกดึงมา
# print(BLUR_IMAGE)
