import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import dotenv_values

env_vars = dotenv_values(".env")
SPEECH_KEY = env_vars["AZURE_TTS"]
SPEECH_REGION = env_vars["AZURE_REGION"]

class SpeechToText:
    def __init__(self):
        print(SPEECH_KEY, SPEECH_REGION)
        self.speech_config = speechsdk.SpeechConfig(subscription=os.environ.get("SPEECH_KEY"), region=os.environ.get("SPEECH_REGION"))
        self.speech_config.speech_recognition_language="en-US"

        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=audio_config)
        pass

    def recognize_from_microphone(self):
        # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"

        print("Speak into your microphone.")
        speech_recognition_result = self.speech_recognizer.recognize_once_async().get()

        if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("Recognized: {}".format(speech_recognition_result.text))
            return speech_recognition_result.text
        elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
        elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_recognition_result.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")

    def recognize_from_file(self, filename):
        audio_input = speechsdk.AudioConfig(filename=filename)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=audio_input)

        result = speech_recognizer.recognize_once_async().get()
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("Recognized: {}".format(result.text))
        elif result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized: {}".format(result.no_match_details))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))

if __name__ == "__main__":
    stt = SpeechToText()
    stt.recognize_from_microphone()
    # stt.recognize_from_file("speech.wav")