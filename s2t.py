"""
For more samples please visit https://github.com/Azure-Samples/cognitive-services-speech-sdk
"""

import os
from urllib.parse import urlparse

import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

load_dotenv()

endpoint_url = os.getenv("AZURE_SPEECH_ENDPOINT")
speech_key = os.getenv("AZURE_SPEECH_KEY")
if not endpoint_url or not speech_key:
    raise RuntimeError(
        "AZURE_SPEECH_ENDPOINT and AZURE_SPEECH_KEY must be set in the .env file."
    )

parsed = urlparse(endpoint_url)
base_endpoint = f"{parsed.scheme}://{parsed.netloc}"

speech_config = speechsdk.SpeechConfig(subscription=speech_key, endpoint=base_endpoint)
speech_config.speech_synthesis_language = "pl-PL"
speech_config.speech_synthesis_voice_name = "en-US-Andrew:DragonHDLatestNeural"

# use the default speaker as audio output.
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

text = "Cześć, witaj w Azure AI Foundry!"

result = speech_synthesizer.speak_text_async(text).get()

# Check result
if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("Speech synthesized for text [{}]".format(text))
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print("Speech synthesis canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        print("Error details: {}".format(cancellation_details.error_details))
