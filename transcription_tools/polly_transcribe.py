import boto3
import os
import datetime
import json
import sys

# Constants
VOICE_ID = 'Joanna'
USAGE_LOG_FILE = 'polly_usage_log.json'
STANDARD_FREE_TIER_LIMIT = 5_000_000  # characters
STANDARD_COST_PER_MILLION = 4.00  # USD
CHAR_LIMIT = 3000  # Polly max input

# Utility Functions
def load_usage_log():
    if os.path.exists(USAGE_LOG_FILE):
        with open(USAGE_LOG_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_usage_log(log):
    with open(USAGE_LOG_FILE, 'w') as f:
        json.dump(log, f, indent=2)

def update_usage(log, chars_used):
    now = datetime.datetime.utcnow()
    key = f"{now.year}-{now.month:02}"
    log[key] = log.get(key, 0) + chars_used
    return log

def estimate_cost(total_chars):
    if total_chars <= STANDARD_FREE_TIER_LIMIT:
        return 0.0
    overage = total_chars - STANDARD_FREE_TIER_LIMIT
    return (overage / 1_000_000) * STANDARD_COST_PER_MILLION

# Entry point
def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {os.path.basename(__file__)} input.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    base, _ = os.path.splitext(input_file)
    output_file = f"{base}.mp3"

    # Read input text
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read().strip()
    except FileNotFoundError:
        print(f"Error: File not found: {input_file}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading {input_file}: {e}")
        sys.exit(1)

    if not text:
        print("Error: Input file is empty.")
        sys.exit(1)

    char_count = len(text)
    print(f"Input file contains {char_count} characters.")

    if char_count > CHAR_LIMIT:
        print(f"Error: Input text exceeds {CHAR_LIMIT} character limit.")
        sys.exit(1)

    # Create Polly client
    try:
        polly = boto3.client('polly')
    except Exception as e:
        print(f"Error initializing Polly client: {e}")
        sys.exit(1)

    # Synthesize speech
    try:
        response = polly.synthesize_speech(
            Text=text,
            OutputFormat='mp3',
            VoiceId=VOICE_ID
        )
    except Exception as e:
        print(f"Error from Polly synthesize_speech: {e}")
        sys.exit(1)

    # Save MP3
    try:
        with open(output_file, 'wb') as file:
            file.write(response['AudioStream'].read())
    except Exception as e:
        print(f"Error saving audio to {output_file}: {e}")
        sys.exit(1)

    print(f"Audio saved to {output_file}")

    # Update usage log
    usage_log = load_usage_log()
    usage_log = update_usage(usage_log, char_count)
    save_usage_log(usage_log)

    # Report usage
    now = datetime.datetime.utcnow()
    key = f"{now.year}-{now.month:02}"
    total_this_month = usage_log.get(key, 0)
    estimated_cost = estimate_cost(total_this_month)

    print(f"Characters used this month: {total_this_month:,}")
    print(f"Estimated cost (standard voice): ${estimated_cost:.2f}")

    if total_this_month > STANDARD_FREE_TIER_LIMIT:
        print("Free tier exceeded.")
    elif total_this_month > STANDARD_FREE_TIER_LIMIT * 0.8:
        print("Warning: Approaching the free tier limit (80%).")

if __name__ == "__main__":
    main()
