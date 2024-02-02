import os
import ast
from dotenv import load_dotenv



def env_data():
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'env.configs')
    load_dotenv(env_path)
    configs = os.environ
    return configs


def get_checkpoint():
    configs = env_data()
    return configs["MODEL_CHECKPOINT"]
def get_batch():
    configs = env_data()
    return ast.literal_eval(configs["BATCH"])

def get_samkwargs():
    configs = env_data()
    if ast.literal_eval(configs["SAM_KWARGS"]) == True :
        kwargs = {
            'points_per_side' : int(configs["POINTS_PER_SIDE"]),
            'points_per_batch': int(os.getenv("POINTS_PER_BATCH")),
            'pred_iou_thresh': float(os.getenv("PRED_IOU_THRESH")),
            'stability_score_thresh': float(os.getenv("STABILITY_SCORE_THRESH")),
            'stability_score_offset': float(os.getenv("STABILITY_SCORE_OFFSET")),
            'box_nms_thresh': float(os.getenv("BOX_NMS_THRESH")),
            'crop_n_layers': int(os.getenv("CROP_N_LAYERS")),
            'crop_nms_thresh': float(os.getenv("CROP_NMS_THRESH")),
            'crop_overlap_ratio': float(os.getenv("CROP_OVERLAP_RATIO")),
            'crop_n_points_downscale_factor': int(os.getenv("CROP_N_POINTS_DOWNSCALE_FACTOR")),
            'min_mask_region_area': int(os.getenv("MIN_MASK_REGION_AREA")),
            'output_mode': os.getenv("OUTPUT_MODE")
                    }
        return kwargs
    else:
        return None
if __name__ == "__main__":
    print(get_checkpoint())