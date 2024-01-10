from geotiff_utility import processimagetif

from image_filter import imagefilter


pro = processimagetif('Image.tif')

print(pro.get_geotiff_transform())



fiter = imagefilter('Image.tif')
fiter.bright_image(0.7)


fiter.imageshow()


