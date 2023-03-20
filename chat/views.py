from django.shortcuts import render, redirect
from chat.models import Room, Message, ChatMessages
from django.http import HttpResponse, JsonResponse
from . forms import ChatMessagesForm

def chat_page(request):
    return render(request, 'chat_home.html')


def chat_section(request):
    return render(request, 'chat_section.html')


def delete_message(request, pk):
    message = ChatMessages.objects.get(pk=pk)
    if request.method == 'DELETE':
        message.delete()
        return HttpResponse('Message deleted.')
        # return redirect('chat_section')


# def chat_home(request):
#     return render(request, 'chat_home.html')


# def room(request, room):
#     username = request.GET.get('username')
#     room_details = Room.objects.get(name=room)
#     return render(request, 'room.html', {
#         'username': username,
#         'room': room,
#         'room_details': room_details
#     })


# def checkview(request):
#     room = request.POST['room_name']
#     username = request.POST['username']

#     if Room.objects.filter(name=room).exists():
#         return redirect('/chat/'+room+'/?username='+username)
#     else:
#         new_room = Room.objects.create(name=room)
#         new_room.save()
#         return redirect('/chat/'+room+'/?username='+username)


# def send(request):
#     message = request.POST['message']
#     username = request.user.username
#     room_id = request.POST['room_id']
#     new_message = Message.objects.create(value=message, user=username, room=room_id)
#     new_message.save()
#     return HttpResponse('Message sent successfully')


# def getMessages(request, room):
#     room_details = Room.objects.get(name=room)
#     messages = Message.objects.filter(room=room_details.id)
#     return JsonResponse({"messages":list(messages.values())})

def chat_messages(request):
    messages = ChatMessages.objects.all()
    context = {'messages': messages}
    return render(request, 'chat_messages.html', context)

def new_chat_message(request):
    # form = ChatMessagesForm()
    # if request.method == 'POST':
    #     form = ChatMessagesForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    user = request.user
    message = request.POST['chat_message']
    new_message = ChatMessages(user=user, message=message)
    new_message.save()
    return redirect('chat_section')
    # context = {'form': form}
    context = {'user': user, 'message': message}
    return render(request, 'chat_messages.html', context)