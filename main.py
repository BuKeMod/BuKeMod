from geotiff_utility import processimagetif

from image_filter import imagefilter


pro = processimagetif('Image.tif')

print(pro.get_geotiff_transform())



fiter = imagefilter('Image.tif')
fiter.bright_image(0.7)


fiter.imageshow()

from samgeo.text_sam import LangSAM


sam = LangSAM()

text_prompt = "fram"

sam.predict(fiter, text_prompt, box_threshold=0.2, text_threshold=0.2)

sam.show_anns(
    cmap='Accent_r',
    box_color='red',
    title=f'Automatic Segmentation of {text_prompt}',
    blend=True,
    # output= f'{output_path}{text_prompt}_detection_boxs.tif'
)

