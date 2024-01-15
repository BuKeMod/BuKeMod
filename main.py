from geotiff_utility import processimagetif
from image_filter import imagefilter
from image_to_image import image_to_tif

# pro = processimagetif('output/1.tif',True)
# pro1 = processimagetif('img/brightened_imagePNG.png',True)
# pro2 = processimagetif('img/brightened_imageTIF.tif',True)



# print(pro.get_geotiff_metadata())
# print(pro1.get_geotiff_crs_pixel())
# print(pro2.get_geotiff_crs_pixel())



fiter = imagefilter('img/Task-of-2023-12-19T112104744Z-orthophoto.tif')
# fiter = imagefilter('img/brightened_imageTIF.tif')

fiter.bright_image(1.2)
print(fiter.get_filename())
fiter.get_num_bands()
fiter.save_image(quality=100)
fiter.save_image_tif(quality=100)

image = fiter.get_image(quality=100)
# fiter.imageshow()

try:

    #
    # from samgeo.text_sam import LangSAM
    #
    #
    # sam = LangSAM()
    #
    # text_prompt = "fram"
    #
    # # sam.predict(fiter, text_prompt, box_threshold=0.2, text_threshold=0.2)
    #
    # # sam.show_anns(
    # #     cmap='Accent_r',
    # #     box_color='red',
    # #     title=f'Automatic Segmentation of {text_prompt}',
    # #     blend=True,
    # #     # output= f'{output_path}{text_prompt}_detection_boxs.tif'
    # # )
    #

    from samgeo import SamGeo

    sam = SamGeo(
        model_type="vit_h",
        # checkpoint="/content/drive/MyDrive/model/epoch-000090-f10.98-ckpt.pth",
        sam_kwargs=None,
    )

    sam_kwargs = {
        "points_per_side": 128,
        "pred_iou_thresh": 0.3,
        "stability_score_thresh": 0.95,
        "crop_n_layers": 1,
        "crop_n_points_downscale_factor": 1,
        "min_mask_region_area": 100,
    }

    mask = "segment_mask.tif"
    sam.generate(
        image, mask, batch=True, foreground=True, erosion_kernel=(3, 3), mask_multiplier=255,
        # sam_kwargs=sam_kwargs
    )

    sam.show_masks(cmap="binary_r")
except Exception as e : print(e)