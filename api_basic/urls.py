from django.urls import path
from .views import voice_to_text

urlpatterns = [
    path('voiceToText/', voice_to_text)
]
