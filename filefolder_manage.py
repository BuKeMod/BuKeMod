import os
import zipfile
import shutil
import glob


def getfilename(file_path):
        directory, filename = os.path.split(file_path)
        name_without_extension = os.path.splitext(filename)[0]
        # return self.filename
        return name_without_extension
def getdirpath(file_path):
        directory, filename = os.path.split(file_path)
        return directory

def copy_img(imgtif_path, output_path='output_folder/'):

    shutil.copy(imgtif_path, output_path)


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
    print('---convert to zip---')
    try:
        zipf = zipfile.ZipFile(f'{zipname}.zip', 'w', zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(output_path):
            for file in files:
                zipf.write(os.path.join(root, file))
        zipf.close()
        print('---convert to zip success---')
    except Exception as e:
        print('folder_to_zip ', e)


# if __name__ == '__main__':
#     copy_img('img\Task-of-2023-12-19T112104744Z-orthophoto.tif','2.tif')