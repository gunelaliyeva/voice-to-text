from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Article
from .serializers import ArticleSerializer
import speech_recognition as sr
import pybase64
import base64

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

        # decote throws error

        # audio = base64.decodestring(data["data"])
        audio_bytes = data["data"].encode('utf-8')
        decoded_data = base64.decodebytes(audio_bytes)
        # print(type(audio))
        audio_file = sr.AudioFile(decoded_data)
        with audio_file as source:
            audio = r.record(source, duration=5)
        return JsonResponse(r.recognize_google(audio), status=200, safe=False)

        # return data

        #
        # return JsonResponse(r.recognize_google(audio), status=200, safe=False)
