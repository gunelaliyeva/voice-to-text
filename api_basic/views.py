import wave
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
import speech_recognition as sr
import base64, os
import soundfile as sf

@csrf_exempt
def voice_to_text(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)

        r = sr.Recognizer()
        r.energy_threshold = 300
        decoded_data = base64.b64decode(data["data"])

        wav_file = wave.open('hello.wav', 'wb')
        wav_file.setnchannels(1)
        wav_file.setframerate(44100.0)
        wav_file.setsampwidth(2)
        wav_file.writeframes(decoded_data)
        wav_file.close()

        harvard = sr.AudioFile('hello.wav')
        with harvard as source:
            audio = r.record(source, duration=5)
        return JsonResponse(r.recognize_google(audio, show_all=True), status=200, safe=False)
