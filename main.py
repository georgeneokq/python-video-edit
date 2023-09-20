from media_editor import sep_audio_video
from media_editor import combine_audio_video
from media_editor import seek_audio
import argparse
import shutil
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('video_path', type=str,
    help='Path to video file')
    parser.add_argument('--seek', type=float, required=True,
    help='Time in seconds for audio seeking. Positive number to play the sound earlier, negative number to play sound later')
    
    args = parser.parse_args()
    seek_time = args.seek
    video_file_path = args.video_path

    output_audio_file_path = sep_audio_video(video_file_path)

    if seek_time is not None:
        output_audio_file_path = seek_audio(output_audio_file_path, seek_time)

    combined_output_file_path = combine_audio_video(video_file_path, output_audio_file_path)

    # Rename "combined" to "shifted"
    output_file_path = f'{"".join(combined_output_file_path.split("-combined.mp4")[:-1])}-shifted.mp4'
    shutil.move(combined_output_file_path, output_file_path)

    print(f'\nExported to {output_file_path}')

    # Clean up temp audio file
    os.remove(output_audio_file_path)


if __name__ == '__main__':
    main()