import os
import zipfile
import shutil
import glob

def getfilename(file_path):
        directory, filename = os.path.split(file_path)
        name_without_extension = os.path.splitext(filename)[0]
        # return self.filename
        return name_without_extension

def setimagepath(folder_path):
    try:
        extension = 'tif'
        if folder_path.endswith(extension):
            image_paths = folder_path
            return image_paths
        else:
            for filename in os.listdir(folder_path):
                if filename.endswith(extension):
                    image_paths = glob.glob(f"{folder_path}/*{extension}")
                    return image_paths
                else:
                    print(f"This is not a {extension} file")
    except Exception as e:
        print('setimagepath ',e)


# create folder
def create_folder(output_path='fiteroutput'):

    # ตรวจสอบว่าโฟลเดอร์มีอยู่หรือไม่
    if not os.path.exists(output_path):
        # ถ้าไม่มี, ให้สร้างโฟลเดอร์
        try:
            os.makedirs(output_path)
        except Exception as e:
            print('create_folder ', e)


# delete folder
def delete_folder(output_path='fiteroutput'):
    try:
        try:

            os.rmdir(output_path)
        except:

            shutil.rmtree(output_path)
    except Exception as e:
        print('delete_folder ', e)


# folder to zip
def folder_to_zip(output_path='fiteroutput', zipname='output_zip'):
    print('add output zip')
    try:
        zipf = zipfile.ZipFile(f'{zipname}.zip', 'w', zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(output_path):
            for file in files:
                zipf.write(os.path.join(root, file))
        zipf.close()
    except Exception as e:
        print('folder_to_zip ', e)


# if __name__ == '__main__':
#     # create_folder()
# #     delete_folder()
# #     folder_to_zip()
