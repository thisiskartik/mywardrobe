from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_201_CREATED
from ai.bot import bot
from .models import Chat


@api_view(['POST'])
def chats(request):
    if 'message' not in request.data:
        return Response({'error': 'Missing data'}, status=HTTP_400_BAD_REQUEST)
    [response, memory] = bot(request.data['message'])
    new_chat = Chat.objects.create(chat_memory=memory)
    return Response({'response': response, 'chat_id': new_chat.id}, status=HTTP_201_CREATED)


@api_view(['PUT'])
def chat(request, chat_id):
    try:
        current_chat = Chat.objects.get(id=chat_id)
    except ObjectDoesNotExist:
        return Response({'error': 'Invalid chat id'}, status=HTTP_404_NOT_FOUND)

    if 'message' not in request.data:
        return Response({'error': 'Missing data'}, status=HTTP_400_BAD_REQUEST)
    [response, new_memory] = bot(request.data['message'], current_chat.chat_memory)
    current_chat.chat_memory = new_memory
    current_chat.save()
    return Response({'response': response}, status=HTTP_200_OK)
