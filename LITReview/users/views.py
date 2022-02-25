from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

# Create your views here.
def loginPage(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            print('Username does not exist')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            print('Username or password is incorrect')


    return render(request, 'users/login_register.html')

def profiles(request):
    return render(request, 'users/profiles.html')