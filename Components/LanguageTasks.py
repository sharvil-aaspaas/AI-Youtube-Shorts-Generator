import anthropic
from dotenv import load_dotenv
import os
import json

load_dotenv()

anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
if not anthropic_api_key:
    raise ValueError("Anthropic API key not found. Make sure it is defined in the .env file.")
client = anthropic.Anthropic(api_key=anthropic_api_key)


# Function to extract start and end times
def extract_clips(json_string):
    try:
        # Parse the JSON string
        data = json.loads(json_string)
        clips = []
        for item in data:
            try:
                title = item.get("title", "Viral Short Clip")
                start_time = int(float(item["start"]))
                end_time = int(float(item["end"]))
                content = item["content"]
                clips.append({
                    "title": title,
                    "start": start_time,
                    "end": end_time,
                    "content": content
                })
            except Exception as e:
                print(f"Error parsing clip: {e}")
        return clips
    except Exception as e:
        print(f"Error in extract_clips: {e}")
        return []


system = """
Based on the Transcription user provides with start and end, highlight the 5 most interesting, non-overlapping parts (clips) of less than 1 minute each, which can be directly converted into shorts. For each clip, do the following:
- Provide the timestamps for the clip to start and end (as seconds or float).
- Write a viral, clickable YouTube Title for that specific clip that would maximize views and engagement. The title should be concise, attention-grabbing, and relevant to the content of the clip.
- Provide the highlight text/content for the clip.

Follow this Format and return in valid JSON (no explanation, no markdown, no extra text):
[
  {
    "title": "Viral and clickable YouTube title for this clip",
    "start": "Start time of the clip",
    "end": "End Time for the highlighted clip",
    "content": "Highlight Text"
  },
  ... (total 5 clips)
]
Return exactly 5 clips, each with its own viral title, a continuous segment. Only return valid JSON, no explanation or extra text.
"""

User = """
Any Example
"""


def GetHighlight(Transcription):
    print("Getting Highlights from Transcription ")
    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            temperature=0.7,
            system=system,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": Transcription + system
                        }
                    ]
                }
            ]
        )
        json_string = message.content[0].text if message.content and hasattr(message.content[0], 'text') else ""
        json_string = json_string.replace("json", "")
        json_string = json_string.replace("```", "")
        clips = extract_clips(json_string)
        if not clips or len(clips) < 5:
            Ask = input("Error - Less than 5 highlights found. Try again? (y/n) -> ").lower()
            if Ask == "y":
                return GetHighlight(Transcription)
        return clips
    except Exception as e:
        print(f"Error in GetHighlight: {e}")
        return []
        return 0, 0


if __name__ == "__main__":
    print(GetHighlight(User))
