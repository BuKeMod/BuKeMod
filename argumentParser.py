
import argparse
def create_parser():
    parser = argparse.ArgumentParser(description='Your program description')


    parser.add_argument('--image_path', type=str, default='images', help='image_path')
    parser.add_argument('--batch', type=bool, default=False, help='predict batch image')
    # Training configuration
    parser.add_argument('--model_type', type=str, default='vit_h', help='model_type segment') 
    

    return parser.parse_args()