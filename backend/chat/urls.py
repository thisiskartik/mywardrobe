from django.urls import path
from .views import chat, chats

urlpatterns = [
    path('', chats),
    path('<str:chat_id>', chat)
]
