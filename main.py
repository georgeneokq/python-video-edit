from media_editor import sep_audio_video
from media_editor import combine_audio_video
from media_editor import seek_audio
import argparse
import json
import os

with open('config.json') as config_file:
    config = json.load(config_file)

output_dir = config['output_dir']

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seek', type=float, required=True,
    help='Time in seconds for audio seeking. Positive number to play the sound earlier, negative number to play sound later')
    parser.add_argument('--video-path', type=str,
    help='Path to video file. If not provided, a dialog for file selection will be shown.')
    
    args = parser.parse_args()
    seek_time = args.seek
    video_file_path = args.video_path
    if video_file_path is None:
        from tkinter import Tk
        from tkinter.filedialog import askopenfilename
        root = Tk()
        root.withdraw() # we don't want a full GUI, so keep the root window from appearing
        root.call('wm', 'attributes', '.', '-topmost', 'True')
        video_file_path = askopenfilename() # show an "Open" dialog box and return the path to the selected file

    if not video_file_path:
        return

    output_audio_file_path = sep_audio_video(video_file_path, output_folder=output_dir)

    if seek_time is not None:
        output_audio_file_path = seek_audio(output_audio_file_path, seek_time)

    combine_audio_video(video_file_path, output_audio_file_path, output_folder=output_dir)


if __name__ == '__main__':
    main()