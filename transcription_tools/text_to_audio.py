import asyncio
from edge_tts import Communicate
import argparse

# FOR A LIST OF VOICES
# edge-tts --list-voices | grep -E '"ShortName": "en-(US|GB)-'

'''
OUTPUT FORMAT OPTIONS
# edge-tts --list-voices | grep -i "audio-" | sort | uniq

Format	                              Description
"audio-24khz-48kbitrate-mono-mp3"	    Default, decent quality MP3
"audio-16khz-32kbitrate-mono-mp3"	    Lower bitrate, smaller size
"audio-48khz-96kbitrate-mono-mp3"	    Higher quality MP3
"raw-24khz-16bit-mono-pcm"	          Raw PCM (for more control)
"webm-24khz-16bit-mono-opus"	        Good for web playback

CLI USAGE
edge-tts --text "Testing audio quality" \
         --voice en-US-GuyNeural \
         --output-format audio-48khz-96kbitrate-mono-mp3 \
         --write-media out.mp3
'''

parser = argparse.ArgumentParser()
parser.add_argument("filename", help = "Text file needed")
args = parser.parse_args()
textfile = args.filename

with open(textfile, "r", encoding="utf-8") as f:
  file_text = f.read()

async def tts():
    communicate = Communicate(
        text=file_text,
        voice="en-GB-RyanNeural",
        rate="-20%",       # slower speech
        pitch="+4Hz",      # slightly higher pitch
        # volume: str = "0dB",
        # output_format: str = "audio-24khz-48kbitrate-mono-mp3"
    )
    await communicate.save("output.mp3")

asyncio.run(tts())
