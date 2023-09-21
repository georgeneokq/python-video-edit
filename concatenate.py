from moviepy.editor import VideoFileClip
import json
import subprocess
import os

with open('config.json') as config_file:
    config = json.load(config_file)

ffmpeg_path = os.path.join(os.getcwd(), config['ffmpeg_path'])
print('[INFO] Using ffmpeg binary from: {}'.format(ffmpeg_path))

def concatenate(video_clip_paths, output_path) -> bool:
    # Assert same dimensions for all videos
    video_clips = [VideoFileClip(clip_path) for clip_path in video_clip_paths]

    expected_width, expected_height = video_clips[0].size
    dimensions_ok = True
    for clip in video_clips[1:]:
        width, height = clip.size

        if width != expected_width or height != expected_height:
            print(f"{clip.filename}: Expected {expected_width}x{expected_height} video, got {width}x{height}")
            dimensions_ok = False

    if not dimensions_ok:
        return False

    video_path_args = ' '.join([f'-i {file_path}' for file_path in video_clip_paths])
    va_args = ' '.join([f'[{i}:v] [{i}:a]' for i in range(len(video_clip_paths))])

    command = f'{ffmpeg_path} {video_path_args} -filter_complex "{va_args} concat=n={len(video_clip_paths)}:v=1:a=1 [v] [a]" -map "[v]" -map "[a]" {output_path}'
    print(f'\n{command}\n')

    # write the output video file
    exit_code = subprocess.call(command, shell=True)

    # Cleanup
    for clip in video_clips:
        clip.close()

    if exit_code == 0:
        return True
    
    return False

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Simple Video Concatenation script in Python with MoviePy Library")
    parser.add_argument("-c", "--clips", nargs="+",
                        help="List of audio or video clip paths")
    parser.add_argument("-o", "--output", help="Output file name")
    args = parser.parse_args()
    clips = args.clips
    output_path = args.output
    success = concatenate(clips, output_path)

    if success:
        print(f"Concatenated video written to {output_path}")
