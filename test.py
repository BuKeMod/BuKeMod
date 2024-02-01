import os
from dotenv import load_dotenv,dotenv_values

configs = dotenv_values(".env.configs")

print(configs['BLUR_IMAGE'])
print(type(configs['BLUR_IMAGE']))