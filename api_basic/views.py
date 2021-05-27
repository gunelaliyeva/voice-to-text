import wave
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
import speech_recognition as sr
import base64

@csrf_exempt
def voice_to_text(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)

        r = sr.Recognizer()
        r.energy_threshold = 300
        decoded_data = base64.b64decode(data["data"])

        file = wave.open('audio.wav', 'wb')
        file.setnchannels(2)
        file.setframerate(44100)
        file.setsampwidth(2)
        file.writeframes(decoded_data)
        file.close()
        harvard = sr.AudioFile('audio.wav')
        with harvard as source:
            audio = r.record(source)
        return JsonResponse(r.recognize_google(audio, show_all=True), status=200, safe=False)
