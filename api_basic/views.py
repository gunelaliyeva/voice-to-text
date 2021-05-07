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

        wav_file = wave.open('hello.wav', 'wb')
        # y = (np.iinfo(np.int32).max * (decoded_data / np.abs(decoded_data).max())).astype(np.int32)
        # print(decoded_data)
        wav_file.setnchannels(1)
        wav_file.setframerate(44100.0 )
        wav_file.setsampwidth(2)
        wav_file.writeframes(decoded_data)
        wav_file.close()
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

        # src = "C:/Users/Gunel/Desktop/diplom isi/voice-to-text/hello.mp3"
        # dst = "hello9.wav"
        #
        # # convert wav to mp3
        # sound = AudioSegment.from_mp3(src)
        # # sound.export(dst, format="wav")

        # AudioSegment.converter = "C:/Users/Gunel/Desktop/diplom isi/voice-to-text/ffmpeg.exe"
        # print(AudioSegment.converter)
        # AudioSegment.ffprobe = os.getcwd() + "\\ffprobe.exe"

        # AudioSegment.converter = "C:/users/gunel/appData/local/programs/python/python36/lib/site-packages/ffmpeg/_ffmpeg"
        # song = AudioSegment.from_mp3(file="hello.mp3")
        # song.export("new.wav", format="wav")

        harvard = sr.AudioFile('hello.wav')
        # # print(type(harvard))
        with harvard as source:
            audio = r.record(source, duration=5)
        #
        # print(r.recognize_google(audio, show_all=True))
        return JsonResponse(r.recognize_google(audio, show_all=True), status=200, safe=False)
        # return JsonResponse('hello', status=200, safe=False)
        #
        # return data

        #
        # return JsonResponse(r.recognize_google(audio), status=200, safe=False)
