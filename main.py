from geotiff_utility import processimagetif
pro = processimagetif('Image.tif')

print(pro.get_geotiff_transform())

