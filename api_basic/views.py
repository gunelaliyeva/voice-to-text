from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Article
from .serializers import ArticleSerializer
import speech_recognition as sr
import pybase64
import base64
import io, wave


@csrf_exempt
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return JsonResponse({"name": "hello"}, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ArticleSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def voice_to_text(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        print(data["data"])

        r = sr.Recognizer()
        r.energy_threshold = 300

        # decode throws error

        # audio = base64.decodestring(data["data"])
        audio_bytes = data["data"].encode('utf-8')
        print(audio_bytes)
        # print(audio_bytes)
        decoded_data = base64.decodebytes(audio_bytes)
        new = base64.b64decode(audio_bytes)

        audio = decoded_data

        # Join wav files

        params_set = False
        temp_file = io.BytesIO()
        with wave.open(temp_file, 'wb') as temp_input:
            for audio_files in audio:
                with wave.open(audio_files, 'rb') as w:
                    if not params_set:
                        temp_input.setparams(w.getparams())
                        params_set = True
                    temp_input.writeframes(w.readframes(w.getnframes()))

        # move the cursor back to the beginning of the "file"
        temp_file.seek(0)
        # Do speech recognition
        binary_audio = temp_file.read()

        audio_file = sr.AudioFile(binary_audio)
        # with audio_file as source:
        #     audio = r.record(source, duration=5)
        return JsonResponse(r.recognize_google(audio_file), status=200, safe=False)
        # return JsonResponse('hello', status=200, safe=False)

        # return data

        #
        # return JsonResponse(r.recognize_google(audio), status=200, safe=False)
