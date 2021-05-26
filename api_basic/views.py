import struct
import wave
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
import speech_recognition as sr
import base64


def genHeader(sampleRate, bitsPerSample, channels, samples):
    datasize = len(samples) * channels * bitsPerSample // 8
    o = bytes("RIFF", 'ascii')  # (4byte) Marks file as RIFF
    o += (datasize + 36).to_bytes(4, 'little')  # (4byte) File size in bytes excluding this and RIFF marker
    o += bytes("WAVE", 'ascii')  # (4byte) File type
    o += bytes("fmt ", 'ascii')  # (4byte) Format Chunk Marker
    o += (16).to_bytes(4, 'little')  # (4byte) Length of above format data
    o += (1).to_bytes(2, 'little')  # (2byte) Format type (1 - PCM)
    o += channels.to_bytes(2, 'little')  # (2byte)
    o += sampleRate.to_bytes(4, 'little')  # (4byte)
    o += (sampleRate * channels * bitsPerSample // 8).to_bytes(4, 'little')  # (4byte)
    o += (channels * bitsPerSample // 8).to_bytes(2, 'little')  # (2byte)
    o += bitsPerSample.to_bytes(2, 'little')  # (2byte)
    o += bytes("data", 'ascii')  # (4byte) Data Chunk Marker
    o += datasize.to_bytes(4, 'little')  # (4byte) Data size in bytes
    return o


def genFile(sampleRate, bitsPerSample, channels, samples):
    header = genHeader(sampleRate, bitsPerSample, channels, samples)
    # print(len(header))
    m = 2**(bitsPerSample - 1) - 1
    int_samples = [int(m * sample) for sample in samples]
    data = struct.pack('<{}l'.format(len(samples)), *int_samples)
    with open("hello4.wav", "wb") as f:
        # f.write(header)
        f.write(samples)




@csrf_exempt
def voice_to_text(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)

        r = sr.Recognizer()
        r.energy_threshold = 300
        decoded_data = base64.b64decode(data["data"], validate=True)

        print(decoded_data)
        # wav_file = wave.open('sound.wav', 'rb')
        # print(wav_file.getnchannels())
        # print(wav_file.getframerate())
        # print(wav_file.getsampwidth())
        # wav_file.write(decoded_data)
        # wav_file.write(genHeader(44100, 16, 1, decoded_data))
        # wav_file.write(decoded_data)
        # wav_file.close()

        # genFile(44100, 16, 2, decoded_data)

        file = wave.open('hello5.wav', 'wb')
        file.setnchannels(2)
        file.setframerate(44100)
        file.setsampwidth(2)
        file.writeframes(decoded_data)
        file.close()
        # open('hi.wav', 'wb').write(decoded_data)
        harvard = sr.AudioFile('hello5.wav')
        with harvard as source:
            audio = r.record(source)
        # return JsonResponse('hello', status=200, safe=False)
        return JsonResponse(r.recognize_google(audio), status=200, safe=False)
