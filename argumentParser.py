
import argparse


def create_parser():
    parser = argparse.ArgumentParser(description='Your program description')

    parser.add_argument('--image_path', type=str,
                        default='images', help='image_path')
    parser.add_argument('--bright', type=int, default=1, help='brightscale')
    parser.add_argument('--batch', default=False, help='predict batch image')
  
    parser.add_argument('--model_type', type=str,
                        default='vit_h', help='model_type segment')

    parser.parse_args().batch = str_to_bool(parser.parse_args().batch)

    return parser.parse_args()


def str_to_bool(s):
    if s == False or s == 'False':
        return False
    elif s == True or s == 'True':
        return True
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


if __name__ == '__main__':
    create_parser()
