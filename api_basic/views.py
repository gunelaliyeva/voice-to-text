from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Article
from .serializers import ArticleSerializer
import speech_recognition as sr
import pybase64
import base64
import wave


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
        # print(data["data"])

        r = sr.Recognizer()
        r.energy_threshold = 300

        # decode throws error

        # audio = base64.decodestring(data["data"])
        # audio_bytes = data["data"].decode('utf-8')
        # print(audio_bytes)
        # print(audio_bytes)
        decoded_data = base64.b64decode(data["data"])
        # print(decoded_data)
        # new = base64.b64decode(audio_bytes)

        # output_file = open('Output.wav', 'wb')
        # output_file.write(decoded_data)
        # output_file.close()
        # print(type(output_file))

        # output_file = wave.open('Output.wav', 'rb')
        # output_file(decoded_data)
        # output_file.close()
        # print(type(output_file))

        sampleRate = 44100.0  # hertz
        duration = 1.0  # seconds
        frequency = 440.0  # hertz
        obj = wave.open('sound.wav', 'wb')
        obj.setnchannels(1)  # mono
        obj.setsampwidth(2)
        obj.setframerate(sampleRate)
        obj.writeframesraw(decoded_data)
        obj.close()

        harvard = sr.AudioFile('sound.wav')
        print(type(harvard))
        with harvard as source:
            audio = r.record(source, duration=5)

        print(r.recognize_google(audio))
        return JsonResponse('hello', status=200, safe=False)
        # return JsonResponse('hello', status=200, safe=False)

        # return data

        #
        # return JsonResponse(r.recognize_google(audio), status=200, safe=False)
