from samgeo.text_sam import LangSAM

sam = LangSAM()
text_prompt = "fram"
outputpath = 'temp'
image = fiter.get_image_temp(outputpath)
print(image)
sam.predict(image, text_prompt, box_threshold=0.2, text_threshold=0.2)
delete_folder(outputpath)
sam.show_anns(
    cmap='Accent_r',
    box_color='red',
    title=f'Automatic Segmentation of {text_prompt}',
    blend=True,
    output=f'detection_boxs.tif'
)