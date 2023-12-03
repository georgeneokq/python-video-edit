# Takes an input video file, creates a copy of it playing in reverse,
# concatenate the original and the copy, convert to GIF

import argparse
import os
from moviepy.editor import VideoFileClip
from moviepy.video.fx.speedx import speedx
from helper import get_basename_from_path, multiglob
from reverse import reverse_video
from concatenate import concatenate
from gif import convert_to_gif

reverse_script = 'reverse.py'
concatenate_script = 'concatenate.py'
gif_script = 'gif.py'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_files', type=str, nargs='+')
    parser.add_argument('-k', '--keep', action='store_true', help='Keep files used to generate the final GIF')
    parser.add_argument('-d', '--duration', type=float, default=2, help='Total duration of boomerang, default 2s')
    args = parser.parse_args()

    input_files = args.input_files
    keep = args.keep
    duration = args.duration

    input_files = multiglob(input_files)
    joined_files_str = '\n'.join(input_files)
    print(f'Processing files:\n{joined_files_str}')

    for input_file in input_files:
        input_file_basename = get_basename_from_path(input_file)

        parent_folders = os.path.dirname(input_file)
        output_file_path = os.path.join(parent_folders, f'{input_file_basename}.gif')

        # Reverse
        reversed_video_path = reverse_video(input_file)

        # Concatenate
        concatenated_clip_path = os.path.join(parent_folders, f'{input_file_basename}-concat.mp4')
        concatenate([input_file, reversed_video_path], concatenated_clip_path)

        concatenated_clip = VideoFileClip(concatenated_clip_path)

        # If duration is specified to be 0, instead use the
        # full length of the video without shortening it.
        if duration != 0:
            clip_path = f'{input_file_basename}-concat-shortened.mp4'
            shortened_clip: VideoFileClip = concatenated_clip.fx(speedx, final_duration=duration)

            print(f'\nGenerating boomerang with duration of {duration} seconds\n')

            # Write the shortened clip to file
            shortened_clip.write_videofile(clip_path)
            shortened_clip.close()
        else:
            clip_path = concatenated_clip_path

        concatenated_clip.close()

        # Convert to gif
        convert_to_gif(clip_path, output_file_path)

        if not keep:
            os.remove(reversed_video_path)
            os.remove(concatenated_clip_path)

            # If not specified to use the full length of the video,
            # there will be an additional shortened video file
            if duration != 0:
                os.remove(clip_path)
