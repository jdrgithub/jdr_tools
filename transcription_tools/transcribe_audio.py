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
result = model.transcribe(input_file_fullpath, temperature=0, verbose=True, fp16=False) 

# Write transcribed text to output file
with open(output_file_fullpath, 'w', encoding="utf-8") as file:
  file.write(result['text']) 
