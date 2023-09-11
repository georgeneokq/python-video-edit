# Takes an input video file, creates a copy of it playing in reverse,
# concatenate the original and the copy, convert to GIF

import argparse
import os
from reverse import reverse
from concatenate import concatenate
from gif import convert_to_gif
from time import sleep

reverse_script = 'reverse.py'
concatenate_script = 'concatenate.py'
gif_script = 'gif.py'


def get_basename_from_path(file_path: str):
    return os.path.basename(file_path).split('.')[0]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=str)
    parser.add_argument('-o', '--output', type=str, required=False, help="Output file path")
    parser.add_argument('-k', '--keep', action='store_true', help='Keep files used to generate the final GIF')
    args = parser.parse_args()

    input_file_path = args.input_file
    output_file_path = args.output
    keep = args.keep

    input_file_basename = get_basename_from_path(input_file_path)

    if output_file_path is None:
        output_file_path = f'{input_file_basename}.gif'

    # Reverse
    reversed_video_path = reverse(input_file_path)

    # Concatenate
    concatenated_video_path = f'{input_file_basename}-concat.mp4'
    concatenate([input_file_path, reversed_video_path], concatenated_video_path)

    # Convert to gif
    convert_to_gif(concatenated_video_path, output_file_path)

    if not keep:
        os.remove(reversed_video_path)
        os.remove(concatenated_video_path)
