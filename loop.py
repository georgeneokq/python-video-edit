import argparse
from moviepy.editor import *
from helper import get_basename_from_path, multiglob


def loop_video(video_path, loop_count):
    video_clip = VideoFileClip(video_path)
    video_clip: VideoFileClip = video_clip.fx(vfx.loop, n=loop_count+1)
    audio_clip = AudioFileClip(video_path)
    audio_clip: AudioFileClip = audio_clip.fx(afx.audio_loop, nloops=loop_count+1)
    final_clip: VideoFileClip = video_clip.set_audio(audio_clip)
    video_file_name = get_basename_from_path(video_path)
    output_file_name = f'{video_file_name}-{loop_count}-l{"s" if loop_count > 1 else ""}.mp4'

    parent_folders = os.path.dirname(video_path)
    output_file_path = os.path.join(parent_folders, output_file_name)
    final_clip.write_videofile(output_file_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_files', type=str, nargs='+')
    parser.add_argument('-n', type=int, default=5, help="Loop count. First playback does not count as a loop.")
    
    args = parser.parse_args()
    input_files = args.input_files
    loop_count = args.n

    if loop_count <= 0:
        print("Loop count should be greater than 0.")
        exit()
    
    input_files = multiglob(input_files)
    joined_files_str = '\n'.join(input_files)
    print(f'Processing files:\n{joined_files_str}')

    for input_file in input_files:
        loop_video(input_file, loop_count)