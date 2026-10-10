# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# -------------------------------------------------------------------------
import azure.cognitiveservices.speech as speechsdk
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('./.env', override=True)

# Set up the speech config using resource endpoint
endpoint_url = os.environ["AZURE_SPEECH_ENDPOINT"]
speech_key = os.environ["AZURE_SPEECH_KEY"]

speech_config = speechsdk.SpeechConfig(
    subscription=speech_key,
    endpoint=endpoint_url,
    speech_recognition_language="pl-PL"
)

# Create a recognizer with microphone input
audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
speech_recognizer = speechsdk.SpeechRecognizer(
    speech_config=speech_config, 
    audio_config=audio_config
)

# Event handlers
def recognized_handler(evt):
    print(f"Recognized: {evt.result.text}")

def recognizing_handler(evt):
    print(f"Recognizing: {evt.result.text}")

# Connect event handlers
speech_recognizer.recognized.connect(recognized_handler)
speech_recognizer.recognizing.connect(recognizing_handler)

# Start continuous recognition
speech_recognizer.start_continuous_recognition()
print("Say something...")

# Keep the program running
input("Press Enter to stop...")
speech_recognizer.stop_continuous_recognition()
