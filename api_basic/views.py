from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Article
from .serializers import ArticleSerializer
import speech_recognition as sr

@csrf_exempt
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return JsonResponse(serializer.data, safe=False)

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
        r = sr.Recognizer()
        r.energy_threshold = 300
        audio_file = sr.AudioFile("")
        with audio_file as source:
            audio = r.record(source, duration=5)

        print(r.recognize_google(audio))
        return JsonResponse(r.recognize_google(audio), status=200, safe=False)