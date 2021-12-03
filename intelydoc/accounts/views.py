from django.core.checks import messages
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
# Create your views here.

def login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']

        user=auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request, user)
            request.session['name'] = username
            #request.session.set_expiry(300)
            return redirect("/")
        else:
            login='failed'
            return render(request, 'login.html',{'login':login,})

    else:
        usernames=[]
        emails=[]
        users = User.objects.all()
        count=0
        for record in users.iterator():
            usernames.append(record.username)
            emails.append(record.email)
            count = count + 1
        return render(request, 'login.html', {'usernames':usernames, 'emails':emails, 'count':count})

def register(request):

    if request.method == 'POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']


        if password1==password2:
            if User.objects.filter(username=username).exists():
                message='Username already taken. Please enter a new Username'
                return render(request,'login.html',{'username_error':message,'autofocus':'autofocus','first_name':first_name,'last_name':last_name,'username':username,'email':email}) 
            elif User.objects.filter(email=email).exists():
                message='Email already exists'
                return render(request,'login.html',{'email_error':message,'autofocus':'autofocus','first_name':first_name,'last_name':last_name,'username':username,'email':email})
            else:
                user= User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password1)
                user.save()
                return redirect('login')               
        else:
            message='Password Not matching'
            return render(request,'login.html',{'pwd_error':message,'autofocus':'autofocus','first_name':first_name,'last_name':last_name,'username':username,'email':email})
        
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')




    