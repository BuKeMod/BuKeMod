import os
import zipfile
import shutil
# create folder


def create_floder(output_path='fiteroutput'):

    # ตรวจสอบว่าโฟลเดอร์มีอยู่หรือไม่
    if not os.path.exists(output_path):
        # ถ้าไม่มี, ให้สร้างโฟลเดอร์
        try:
            os.makedirs(output_path)
        except Exception as e:
            print('create_floder ', e)
# delete folder


def delete_floder(output_path='fiteroutput'):
    try:
        try:

            os.rmdir(output_path)
        except:

            shutil.rmtree(output_path)
    except Exception as e:
        print('delete_floder ', e)


# floder to zip
def floder_to_zip(output_path='fiteroutput', zipname='output_zip'):
    try:
        zipf = zipfile.ZipFile(f'{zipname}.zip', 'w', zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(output_path):
            for file in files:
                zipf.write(os.path.join(root, file))
        zipf.close()
    except Exception as e:
        print('floder_to_zip ', e)
