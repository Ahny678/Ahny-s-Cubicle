from django.shortcuts import render, redirect
from .models import Bword, Message, Room
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User, auth
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
import re

# Create your views here.

def normalize(message):
    #removes extra whitespace characters in the middle
    message = re.sub('\s+', ' ', message)
    #removes leading and trailing whitespace charcters
    message = message.strip()
    return message

def filter(message, list):
    #apply regex filtering on message
    pattern = re.compile('|'.join(list),re.IGNORECASE)
    message = normalize(message)
    if pattern.search(message):
        return True
    else:
        return False


def sendEmail(request, username, ww, bw, ee):
    subject = 'Guideline Breach'
    message =  f'''
     Hello, {username},
     This email has been sent to notify you that you have breached our chat server's guideline
     This is most likely due to your excess use of restrcited words in the chat
     The following words are of level 1 restriction : {', '.join(ww)}
     The following words are of level 2 restriction : {', '.join(bw)}
     The following words are of level 3 restriction : {', '.join(ee)}
     Note: Using a Level 3 word once gets you directly kicked out
           Using a Lvel 2 word thrice gets you kicked out
     Please adhere to our guidelines
     Sincerely, 
     Cubicle Ops Team
    '''

    recepient_email = 'request.user.email'

    try:
        send_mail(subject, message, 'settings.EMAIL_HOST_USER',recipient_list=[recepient_email], fail_silently=False)
        return HttpResponse('Email sent successfully')
    except Exception as e:
        return HttpResponse(f'Error sending mail: {e}')


def chatChecker(request):
    keyword = 'Extreme'
    keyword1 = 'Bad'
    keyword2 = 'Wrong'
    #collect data from database and store in lists
    extreme_words= [bword.name for bword in Bword.objects.filter(category__name=keyword) ]
    bad_words = [bword.name for bword in Bword.objects.filter(category__name=keyword1) ]
    wrong_words = [bword.name for bword in Bword.objects.filter(category__name=keyword2) ]

    #collect the message from form
    if request.method=='POST':
        username = request.POST.get('username')
        message = request.POST.get('message')
        ex_val = filter(message, extreme_words)
        bad_val = filter(message, bad_words)
        wrong_val = filter(message, wrong_words)

        if ex_val:
            messages.info(request, 'this is a extreme word')
            sendEmail(request, username, wrong_words, bad_words, extreme_words)
            return JsonResponse({'redirect_url': '/jail'})
        elif wrong_val:
            messages.info(request, 'this is a wrong word')
        elif bad_val:
            if 'warning_count' not in request.session:
                request.session['warning_count'] = 1
                messages.info(request, 'this is a bad word')
            else:
                request.session['warning_count'] += 1
                messages.info(request, 'this is a bad word')

            if request.session['warning_count']>=3:
                del request.session['warning_count']
                sendEmail(request, username, wrong_words, bad_words, extreme_words)
                return JsonResponse({'redirect_url': '/jail'})
        
        storage = messages.get_messages(request)  # Get messages as storage
        message_list = [str(m) for m in storage]  # Convert messages to string

        # Return messages as part of the JSON response
        return JsonResponse({'messages': message_list})
       

    return JsonResponse({'error': 'Invalid request method'})

def jail(request):
    return render(request, 'jail.html')


def Jumpin(request):
    if request.method =='POST':
        username=request.POST['username']
        roomname=request.POST['roomname']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
         
        if user is not None:
             auth.login(request, user)

             if Room.objects.filter(name=roomname).exists():
                return redirect('/'+roomname+'/?username='+username)
             else:
                new_room=Room.objects.create(name=roomname)
                new_room.save()
                return redirect('/'+roomname+'/?username='+username) 
        else:
             messages.info(request, 'Credentials does not exist')
             return redirect('/')          

            

        
    return render(request, 'Jumpin.html')

def Register(request):
     if request.method == 'POST':
         username = request.POST['username']
         email = request.POST['email']
         password = request.POST['password']
         password1 = request.POST['password1']

         if password==password1:
              if  User.objects.filter(email=email).exists():
                  messages.info(request, 'Email already exists')
                  return redirect('Register')
              elif User.objects.filter(username=username).exists():
                  messages.info(request, 'username already exists')
                  return redirect('Register')
              else:
                  user = User.objects.create_user(username=username, email=email, password=password)
                  user.save()
                  return redirect('/')
                  
         else:
             messages.info(request, 'Password mismatch')
             return redirect('Register') 
     return render(request, 'Register.html')

def TheRoom(request,chatroom):
    #first relay info to html page
    username = request.GET.get('username')
    chatroom_details = Room.objects.get(name=chatroom)
    context = {
        'username' : username,
        'chatroom_details' : chatroom_details,
        'chatroom': chatroom
    }

    return render(request, 'Room.html', context)
    
def PostMessages(request):
    #then get the info from html page
    #if request.method == 'POST':
    message= request.POST['message']
    myUser = request.POST['username']
    room_name = request.POST['room_name']

    Sroom = Room.objects.get(name=room_name)
    new_message = Message.objects.create(room=Sroom,text=message,user=myUser)
    new_message.save()

def getMessages(request, chatroom):
    room_details = Room.objects.get(name=chatroom)
    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages": list(messages.values())})