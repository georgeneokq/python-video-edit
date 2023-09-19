# Takes an input video file, creates a copy of it playing in reverse,
# concatenate the original and the copy, convert to GIF

import argparse
import os
from moviepy.editor import VideoFileClip
from moviepy.video.fx.speedx import speedx
from reverse import reverse
from concatenate import concatenate
from gif import convert_to_gif

reverse_script = 'reverse.py'
concatenate_script = 'concatenate.py'
gif_script = 'gif.py'
DEFAULT_DURATION = 2

def get_basename_from_path(file_path: str):
    return os.path.basename(file_path).split('.')[0]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=str)
    parser.add_argument('-o', '--output', type=str, required=False, help="Output file path")
    parser.add_argument('-k', '--keep', action='store_true', help='Keep files used to generate the final GIF')
    parser.add_argument('-d', '--duration', type=float, help='Total duration of boomerang, default 2s')
    args = parser.parse_args()

    input_file_path = args.input_file
    output_file_path = args.output
    keep = args.keep
    duration = args.duration

    input_file_basename = get_basename_from_path(input_file_path)

    if output_file_path is None:
        output_file_path = f'{input_file_basename}.gif'

    # Reverse
    reversed_video_path = reverse(input_file_path)

    # Concatenate
    concatenated_video_path = f'{input_file_basename}-concat.mp4'
    concatenate([input_file_path, reversed_video_path], concatenated_video_path)

    # Shorten to specified number of seconds, by default 2
    final_duration = duration if duration is not None else DEFAULT_DURATION
    clip = VideoFileClip(concatenated_video_path)
    shortened_clip_path = f'{input_file_basename}-concat-shortened.mp4'
    shortened_clip: VideoFileClip = clip.fx(speedx, final_duration=final_duration)

    # Write the shortened clip to file
    shortened_clip.write_videofile(shortened_clip_path)

    # Cleanup
    clip.close()
    shortened_clip.close()

    # Convert to gif
    convert_to_gif(shortened_clip_path, output_file_path)

    if not keep:
        os.remove(reversed_video_path)
        os.remove(concatenated_video_path)
        os.remove(shortened_clip_path)
