# Create your views here.

from .models import Room, Topic, Message
from .forms import RoomForm, UserForm
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def registerUser(request):

    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'an error occurred during registration')

    data = {'form': form}
    return render(request, 'base/signup.html', data)


def loginUser(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'user doesn\'t exist')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:   
            messages.error(request, 'wrong username or password')

    return render(request, 'base/login.html')


def logoutUser(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', id=user.id)

    data = {'form': form}
    return render(request, 'base/update-user.html', data)



def home(request):          

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
            Q(topic__name__icontains=q) |
            Q(name__icontains=q) |
            Q(description__icontains=q)
        )     
    topics = Topic.objects.all()[0:5]
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    
    data = {'rooms': rooms, 'topics': topics, 'room_count': rooms.count(), 'room_messages': room_messages}
    return render(request, 'base/home.html', data)


def userProfile(request, id):
    user = User.objects.get(id=id)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    data = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics, 'room_count': rooms.count()}
    return render(request, 'base/profile.html', data)

def room(request, id):

    room = Room.objects.get(id=id)

    if request.method == 'POST':
        Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', id=id)

    room_messages = room.message_set.all()
    participants = room.participants.all()

    data = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', data)


@login_required(login_url='login')
def createRoom(request):

    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )

        return redirect('home')

    data = {'form': form, 'topics': topics}
    return render(request, 'base/room-form.html', data)


@login_required(login_url='login')
def updateRoom(request, id):

    room = Room.objects.get(id=id)
    topics = Topic.objects.all()


    if request.user != room.host:
        return HttpResponse('You are not allowed here')

    form = RoomForm(instance=room)

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('room', room.id)

    data = {'form': form, 'topics': topics, 'room': room }
    return render(request, 'base/room-form.html', data)


@login_required(login_url='login')
def deleteRoom(request, id):

    room = Room.objects.get(id=id)

    if request.user != room.host:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    data = {'obj': room}
    return render(request, 'base/delete.html', data)


@login_required(login_url='login')
def deleteMessage(request, id):

    message = Message.objects.get(id=id)

    if request.user != message.user:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        message.delete()
        return redirect('room', message.room.id)
    
    data = {'obj': message}
    return render(request, 'base/delete.html', data)

def topicsPage(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    topics = Topic.objects.filter(name__icontains=q)

    return render(request, 'base/topics.html', {'topics': topics})

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})