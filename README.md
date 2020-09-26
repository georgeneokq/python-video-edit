% Python-Video-Edit

## What's this?
A python program I created to synchronize audio of video files.

I was watching a video and the audio was obviously lacking behind. I wanted to find a simple console program to adjust the audio as I didn't want to download some huge software just to complete the task. I couldn't find one that suited my needs (or maybe I just didn't search hard enough) so I decided to take matters into my own hands.

This program has only been tested for Windows.

## Usage
python main.py [--seek] SEEK [--video-path] VIDEO-PATH

Where SEEK is a number in seconds and VIDEO-PATH is the full path to the video.

SEEK is a required parameter.

VIDEO-PATH is not required but currently recommended (see "Issues" section below). If VIDEO-PATH is not provided, a file selection dialog will be shown.

Example usage:
``` python main.py --seek 10 --video-path C:\Users\USERNAME\my_video.mp4 ```

The above command will take the specified video and adjust its audio to start right away from the original 10 second mark. The video will be saved into this project's "output" folder, but the destination folder can be changed by changing the value of "output_dir" in the config.json file.

## Dependencies
- tk
- moviepy
- numpy
- scipy
- ffmpeg (binary provided in "bin" folder)

To install all dependencies using pip:

```pip install -U tk moviepy numpy scipy```


## Issues
After running this program a few times (roughly 5 times) tkinter's ```askopenfiledialog``` function will cease to work.

It will then start to freeze other running processes. A computer restart fixes the problem, but there are cases where the issue fixes itself over time. It is currently recommended to directly provide the video file path to the program using the --video-path option on the command line to avoid the usage of the file dialog.