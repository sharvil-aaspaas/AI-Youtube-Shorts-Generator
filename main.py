from Components.YoutubeDownloader import download_youtube_video
from Components.Edit import extractAudio, crop_video
import burn_wordlevel_subs
from Components.Transcription import transcribeAudio
from Components.LanguageTasks import GetHighlight
from Components.FaceCrop import crop_to_vertical, combine_videos

url = input("Enter YouTube video URL (leave blank to use existing video and transcription): ").strip()

if url:
    Vid = download_youtube_video(url)
    if Vid:
        Vid = Vid.replace(".webm", ".mp4")
        print(f"Downloaded video and audio files successfully! at {Vid}")

        Audio = extractAudio(Vid)
        if Audio:
            transcriptions = transcribeAudio(Audio)
            if len(transcriptions) > 0:
                TransText = ""
                for text, start, end in transcriptions:
                    TransText += (f"{start} - {end}: {text}")
                # Save transcription to file
                with open("transcription.txt", "w", encoding="utf-8") as f:
                    f.write(TransText)
                print("Transcription saved to transcription.txt")
                # Continue to highlight/clip workflow below
            else:
                print("No transcriptions found")
                exit(1)
        else:
            print("No audio file found")
            exit(1)
    else:
        print("Unable to Download the video")
        exit(1)
    transcription_path = "transcription.txt"
    video_path = Vid
else:
    video_path = input("Enter path to video file (e.g., MyVideo.mp4): ").strip()
    transcription_path = input("Enter path to transcription file (e.g., transcription.txt): ").strip()

# Load transcription
try:
    with open(transcription_path, "r", encoding="utf-8") as f:
        TransText = f.read()
    print(f"Loaded transcription from {transcription_path}")
except Exception as e:
    print(f"Failed to load transcription: {e}")
    exit(1)

# Generate highlights and clips
clips = GetHighlight(TransText)
from re import sub

def sanitize_filename(name):
    sanitized = sub(r'[^\w\-_ ]', '', name).strip().replace(' ', '_')
    return sanitized[:80] if sanitized else 'viral_short_clip'

if clips and len(clips) == 5:
    output_files = []
    for idx, clip in enumerate(clips):
        start = clip["start"]
        stop = clip["end"]
        content = clip["content"]
        title = clip.get("title", f"Clip {idx+1}")
        sanitized_title = sanitize_filename(title)
        print(f"Clip {idx+1}: Title: {title}\n  Start: {start}, End: {stop}\n  Content: {content}\n")

        output_base = f"{sanitized_title}"
        out_video = f"{output_base}_out.mp4"
        cropped_video = f"{output_base}_cropped.mp4"
        final_video = f"{output_base}.mp4"
        subtitled_video = f"{output_base}_subtitled.mp4"

        crop_video(video_path, out_video, start, stop)
        crop_to_vertical(out_video, cropped_video)
        combine_videos(out_video, cropped_video, final_video)

        # Burn word-by-word subtitles using burn_wordlevel_subs
        wordsubs_video = f"{output_base}_wordsubs.mp4"
        burn_wordlevel_subs.burn_wordlevel_subs(final_video, wordsubs_video)
        print(f"Word-level subtitles burned into {wordsubs_video}")
        output_files.append(wordsubs_video)

    print("\nAll 5 clips processed. Final output files:")
    for f in output_files:
        print(f)
else:
    print("Error: Did not get 5 highlight clips from the AI.")