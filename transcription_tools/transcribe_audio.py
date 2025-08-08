import whisper # pip install openai-whisper
import argparse
import os

'''
Keep expectations realistic
On CPU, here’s a rough idea of transcription times for 30 minutes of audio:

Model	Est. Time (CPU)
tiny	5–10 min
base	10–15 min
small	15–25 min
medium	1.5–3 hours
large	Don’t even try

TO NORMALIZE: ffmpeg -i /mnt/h/TECH/INTERVIEWS/Audio_07_31_2025_09_53_39.mp3  -ac 1 -ar 16000 -c:a pcm_s16le Audio_07_31_2025_09_53_39.wav 

1. Audio Input Issues
Whisper is extremely sensitive to the audio it receives.

Common problems:
Silent or nearly silent audio: Whisper can "hallucinate" or repeat filler phrases if the audio is quiet or silent. Check if the waveform is flat.

Non-speech audio: If there's music, background noise, or unclear speech, it may confuse the model.

Wrong sampling rate or encoding: Audio should ideally be mono, 16-bit PCM, 16kHz or 24kHz WAV/FLAC. MP3 or WebM might introduce artifacts.

Fixes:
Normalize volume (ffmpeg -af loudnorm)

Convert to WAV PCM format:
ffmpeg -i input.mp3 -ac 1 -ar 16000 -c:a pcm_s16le output.wav
Play it back yourself and verify that it’s clean and contains actual speech throughout.

2. Bad Decoding Settings or Over-aggressive Temperature
Whisper has a few decoding parameters like:
  temperature, beam_size, and best_of. 
If decoding fails early (e.g., with token repetition), increasing TEMPERATURE helps reduce repetition.

Try this:
result = model.transcribe(audio_path, temperature=0.4)
If you use beam search, try switching back to greedy decoding temporarily.

3. Long Silence Early in Audio
If the model starts transcribing silence or filler noises at the beginning, it may get into a loop. Try trimming the initial silence:
ffmpeg -i input.wav -af silenceremove=1:0:-50dB trimmed.wav

Or crop the first few seconds:
ffmpeg -ss 00:00:03 -i input.wav -c copy cropped.wav

4. Log Probabilities / No-speech Detection
The model may be detecting "no speech" but you’re overriding that.

In whisper.transcribe(), try:
result = model.transcribe(audio_path, no_speech_threshold=0.6, logprob_threshold=-1.0)

5. Try --fp16 False or use device="cpu"
If you're on an environment with half-precision (e.g., GPU inference with fp16=True), 
sometimes you get weird issues due to NaNs or underflow—especially on longer files. Try forcing CPU or full precision:

model = whisper.load_model("medium", device="cpu")
result = model.transcribe(audio_path, fp16=False)

6. The no_speech_threshold parameter in Whisper's transcribe() function
controls how sensitive the model is to detecting actual speech vs silence or noise. 
It's used to help skip segments that contain no meaningful speech.

🔍 no_speech_threshold — What It Means
It works together with Whisper’s voice activity detection (VAD).
Each segment has an associated no_speech_prob — the model’s internal guess of whether there's no speech.
If no_speech_prob > no_speech_threshold, that segment will be skipped (treated as silence).
You control that cutoff with no_speech_threshold.

📊 Practical Values
Threshold	Behavior
0.0	Never skip — transcribe everything, even silence or static
0.3	Default — reasonably permissive (often keeps quiet segments with low confidence)
0.6	Stricter — skip anything unless the model is confident there's speech
0.9	Very strict — great if there's lots of background noise or music

🧠 Why You Might Use no_speech_threshold=0.6
You’re seeing repetition, filler words, or hallucinated speech like "Okay okay okay"
This often happens when the model thinks there’s speech but isn’t sure.
Increasing this threshold helps ignore low-confidence, non-speech segments.
Especially useful in interviews where there are long pauses, coughs, typing, etc.

✅ Example Usage
In your Python script:

result = model.transcribe(
    input_file_fullpath,
    temperature=0.4,
    fp16=False,
    language="en",
    no_speech_threshold=0.6
)

Or add to transcribe_args in the dictionary like:
transcribe_args["no_speech_threshold"] = 0.6
'''

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="this needs an mp3 filename")
parser.add_argument("--file_dir", default="/mnt/h/TECH/INTERVIEWS/", help="Directory for the input .mp3 file")
parser.add_argument("--output_dir", default="/mnt/h/TECH/INTERVIEWS/", help="Directory for the output .txt file")
parser.add_argument("--model", default="base", help="Whisper model size (e.g. base, medium, large)")
parser.add_argument("--language", help="Force language (e.g., 'en')")
parser.add_argument("--verbose", action="store_true", help="Enable debug messages")

args = parser.parse_args()
input_file = args.filename
input_dir = args.file_dir
output_dir = args.output_dir

# Convert input .mp3 filename to output.txt
base_name = os.path.splitext(os.path.basename(input_file))[0]

# Input full path
input_file_fullpath = output_dir + input_file

# Output file and directory
output_file = base_name + ".txt"
output_file_fullpath = output_dir + output_file

# Whisper docs
# https://github.com/openai/whisper

model = whisper.load_model("small.en")  # there is small, medium
# temperature controls randomness of transcription
# 1.0 is more random
# 0.0 is most deterministic.  more confident
# use when hallucinating
result = model.transcribe(
  input_file_fullpath, 
  temperature=0, 
  verbose=True, 
  fp16=False,
  no_speech_threshold=0.6
  ) 

# Write transcribed text to output file
with open(output_file_fullpath, 'w', encoding="utf-8") as file:
  file.write(result['text']) 
