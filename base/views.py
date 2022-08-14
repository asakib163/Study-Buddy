from django.http import HttpResponse
from django.shortcuts import redirect, render
from matplotlib.style import context
from base.forms import RoomForm, UserForm
from django.db.models import Q
from base.models import Message, Rooom, Topic, User
from django.contrib import messages
from base.forms import MyUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST['email'].lower()
        password = request.POST['password']
        try:
            user = User.objects.get(email = email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email = email, password = password)
        if user is not None:
            login(request, user )
            return redirect('home')
        else:
            messages.error(request, 'password is wrong!')

    context = {
        'page' : page,
    }
    return render(request, 'login_register.html', context)

def logoutuser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    page = 'register'
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.email = user.email.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration!')
    context = {
        'page' : page,
        'form' : form,
    }
    return render(request, 'login_register.html', context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    room = Rooom.objects.filter(
        Q(topic__name__icontains = q)|
        Q(name__icontains = q)|
        Q(description__icontains = q)
    )
    room_count = room.count()
    topic = Topic.objects.all()[0:5]
    room_messages = Message.objects.filter(Q(room__topic__name__icontains = q))
    context = {
        'rooms' : room,
        'topics' : topic,
        'room_count' : room_count,
        'room_messages' : room_messages,
    }
    
    return render(request, 'home.html', context)

def room(request, pk ):
    room = Rooom.objects.get(id =pk)
    room_messages = room.message_set.all().order_by('created')
    participants = room.participants.all()
    if request.method == "POST":
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST['body']
        )
        room.participants.add(request.user)
        return redirect('room', pk = room.id)
    
    context = {
        'room' : room, 
        'room_messages' : room_messages,
        'participants' : participants,
    }
    return render(request, 'room.html', context)


def userprofile(request, pk):
    user = User.objects.get(id = pk)
    rooms = user.rooom_set.all()
    topic = Topic.objects.all()
    room_messages = user.message_set.all().order_by('created')
    
    context = {
        'user': user,
        'rooms' : rooms,
        'topics' : topic,
        'room_messages': room_messages,
    }
    return render(request, "profile.html", context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST['topic']
        topic, created = Topic.objects.get_or_create(name = topic_name)
        Rooom.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST['name'],
            description = request.POST['description']
        )
        return redirect('home')
    context = {
        'roomform' : form,
        'topics' : topics,
    }
    return render(request, 'create-room.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Rooom.objects.get(id=pk)
    form  = RoomForm(instance=room)
    topics = Topic.objects.all()
    page = 'update'
    if request.user != room.host:
        return HttpResponse('You are not admin here')

    if request.method == 'POST':
        topic_name = request.POST['topic']
        topic, created = Topic.objects.get_or_create(name = topic_name)
        
        room.name = request.POST['name']
        room.topic = topic
        room.description = request.POST['description']
        room.save()
        return redirect('home')

    context = {
        'roomform' : form,
        'topics' : topics,
        'room' : room,
        'page' : page,
    }
    print(page)
    return render(request, 'create-room.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Rooom.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You are not admin here')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    return render(request, 'delete.html', {'obj':room})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('You are not allowed here!')
    if request.method == 'POST':
        message.delete()
        return redirect('room', pk = message.room.id)
    
    return render(request, 'delete.html', {'obj':message})


@login_required(login_url = 'login')
def updateUser(request):
    user = request.user
    form  = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST,request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('userprofile', pk = user.id)
    context = {
        'form' : form,
    }
    return render(request, 'update-user.html', context)

def topicpage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains = q)
    context = {
        'topics' : topics,
    }
    return render(request, 'topics.html', context)

def activitypage(request):
    room_messages = Message.objects.all()
    context = {
        'room_messages' : room_messages,
    }
    return render(request, 'activity.html', context)