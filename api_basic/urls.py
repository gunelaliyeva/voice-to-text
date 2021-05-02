from django.urls import path
from .views import article_list, voice_to_text

urlpatterns = [
    path('article/', article_list),
    path('voiceToText/', voice_to_text)
]
