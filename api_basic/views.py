from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Article
from .serializers import ArticleSerializer
import speech_recognition as sr
import ffmpeg
from scipy.io import wavfile
from playsound import playsound
import pybase64
import base64
import wave
import numpy as np


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
        # audio_bytes = data["data"].decode('utf-8')
        # print(audio_bytes)
        # print(audio_bytes)
        decoded_data = base64.b64decode(data["data"])
        # print(decoded_data)
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

        # sampleRate = 44100.0  # hertz
        # obj = wave.open('temp.wav', 'wb')
        # obj.setnchannels(1)  # mono
        # obj.setsampwidth(2)
        # obj.setframerate(sampleRate)
        # obj.writeframes(decoded_data)
        # obj.close()

        # obj = wave.open('sound.wav', 'r')

        wav_file = open('hello.wav', 'wb')
        # y = (np.iinfo(np.int32).max * (decoded_data / np.abs(decoded_data).max())).astype(np.int32)
        # print(decoded_data)
        # wav_file.setnchannels(2)
        # wav_file.setsampwidth(2)
        wav_file.write(decoded_data)
        # wav_file.close()
        # print(type(open('sound.wav')))
        # playsound(wav_file.name)
        # wave.open(wav_file)
        # print(wav_file.name)

        # samplerate = 44100
        # fs = 100
        # t = np.linspace(0., 1., samplerate)
        # amplitude = np.iinfo(np.int16).max
        # data = amplitude * np.sin(2. * np.pi * fs * t)
        # write("temp3.wav", samplerate, data.astype(np.int16))
        #
        # playsound('temp3.wav')

        # y = (np.iinfo(np.int32).max * (decoded_data / np.abs(decoded_data).max())).astype(np.int32)

        # wavfile.write('temp.wav', y)

        # stream = ffmpeg.input('temp.wav')
        # stream = ffmpeg.output(stream, 'temp5.wav')
        # print(stream)

        harvard = sr.AudioFile('hello.wav')
        # # print(type(harvard))
        with harvard as source:
            audio = r.record(source, duration=5)
        #
        # print(r.recognize_google(audio))
        return JsonResponse(r.recognize_google(audio), status=200, safe=False)
        # return JsonResponse('hello', status=200, safe=False)

        # return data

        #
        # return JsonResponse(r.recognize_google(audio), status=200, safe=False)
