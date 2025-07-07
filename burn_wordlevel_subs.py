import sys
import os
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from Components.Transcription import transcribeAudio

def transcribe_wordlevel(audio_path):
    """
    Transcribe audio with word-level timestamps using faster-whisper (if supported), else fallback to segment-level.
    Returns a list of dicts: [{"word": str, "start": float, "end": float}]
    """
    try:
        from faster_whisper import WhisperModel
        model = WhisperModel("base.en")
        segments, _ = model.transcribe(audio_path, word_timestamps=True)
        word_timings = []
        for segment in segments:
            for word in segment.words:
                word_timings.append({
                    "word": word.word,
                    "start": word.start,
                    "end": word.end
                })
        return word_timings
    except Exception as e:
        print("Word-level transcription failed, falling back to segment-level. Error:", e)
        # fallback to segment-level
        segs = transcribeAudio(audio_path)
        word_timings = []
        for text, start, end in segs:
            word_timings.append({"word": text, "start": start, "end": end})
        return word_timings

def extract_audio_from_video(video_path, audio_path):
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path)
    clip.close()

def burn_wordlevel_subs(video_path, output_path):
    temp_audio = "temp_wordlevel_audio.wav"
    extract_audio_from_video(video_path, temp_audio)
    word_timings = transcribe_wordlevel(temp_audio)
    video = VideoFileClip(video_path)
    subtitle_clips = []
    from moviepy.video.tools.drawing import color_split
    for word in word_timings:
        txt = word["word"]
        start = word["start"]
        end = word["end"]
        if start is not None and end is not None:
            txt_clip = TextClip(
                txt,
                fontsize=int(video.h * 0.08),
                font='DejaVuSans-Bold',
                color='white',
                method='caption',
                size=(int(video.w * 0.85), None),
                align='center',
                print_cmd=False
            )
            txt_clip = txt_clip.set_start(start).set_end(end).set_position(("center", int(video.h*0.77)))
            subtitle_clips.append(txt_clip)
    final = CompositeVideoClip([video] + subtitle_clips)
    final.write_videofile(output_path, codec='libx264', audio_codec='aac')
    os.remove(temp_audio)
    print(f"Word-level subtitles burned to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python burn_wordlevel_subs.py <input_video> <output_video>")
        sys.exit(1)
    input_video = sys.argv[1]
    output_video = sys.argv[2]
    burn_wordlevel_subs(input_video, output_video)
