from django.contrib import admin
from django.urls import path, include


# urls.py

from django.urls import path
from .views import gemini_chat

urlpatterns = [
    path("chatbot/", gemini_chat, name="gemini_chat"),
]
