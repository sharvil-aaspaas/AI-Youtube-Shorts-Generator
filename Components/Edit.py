from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import VideoFileClip
import subprocess

def extractAudio(video_path):
    try:
        video_clip = VideoFileClip(video_path)
        audio_path = "audio.wav"
        video_clip.audio.write_audiofile(audio_path)
        video_clip.close()
        print(f"Extracted audio to: {audio_path}")
        return audio_path
    except Exception as e:
        print(f"An error occurred while extracting audio: {e}")
        return None


def crop_video(input_file, output_file, start_time, end_time):
    with VideoFileClip(input_file) as video:
        cropped_video = video.subclip(start_time, end_time)
        cropped_video.write_videofile(output_file, codec='libx264')

def burn_subtitles_to_video(input_video, subtitles, output_video):
    """
    input_video: path to the video file
    subtitles: list of (text, start, end) tuples (in seconds)
    output_video: path to save the output video with burned-in subtitles
    """
    from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
    video = VideoFileClip(input_video)
    subtitle_clips = []
    for text, start, end in subtitles:
        txt_clip = TextClip(text, fontsize=36, color='white', font='Arial-Bold', stroke_color='black', stroke_width=2, method='caption', size=(video.w * 0.9, None), align='South')
        txt_clip = txt_clip.set_start(start).set_end(end).set_position(('center', 'bottom'))
        subtitle_clips.append(txt_clip)
    final = CompositeVideoClip([video] + subtitle_clips)
    final.write_videofile(output_video, codec='libx264', audio_codec='aac')

# Example usage:
if __name__ == "__main__":
    input_file = r"Example.mp4" ## Test
    print(input_file)
    output_file = "Short.mp4"
    start_time = 31.92 
    end_time = 49.2   

    crop_video(input_file, output_file, start_time, end_time)

