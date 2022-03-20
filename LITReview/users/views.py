from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.auth.models import User

from base.forms import ProjectForm
from base.models import Project
from base.views import project
from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm, SkillForm



# Create your views here.
def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'Username or password is incorrect')

    return render(request, 'users/login_register.html')


def logoutUser(request):
    logout(request)
    messages.error(request, 'User was logged out')
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created')

            login(request, user)
            return redirect('edit-account')

        else:
            messages.success(request, 'An error has occurred during registration')

    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)


def profiles(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

   
    profiles = Profile.objects.filter(name__icontains=search_query)
    context = {'profiles': profiles}
    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    profile2 = request.user.profile
    topInterests = profile.skill_set.exclude(description__exact="")
    otherInterests = profile.skill_set.filter(description="")
    if request.method == 'POST': 
        if request.user.profile.favourites.exists():
            profile2.favourites.remove(profile)
        else:
            profile2.favourites.add(profile)
        
      

    context = {'profile': profile, 'topInterests': topInterests, "otherInterests": otherInterests}
    return render(request, 'users/user-profile.html', context)


@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    interests = profile.skill_set.all()
    projects = profile.project_set.all()
    

    context = {'profile': profile, 'interests': interests, 'projects': projects}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')

    context = {'form': form}
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def createInterest(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/interest_form.html', context)


@login_required(login_url='login')
def updateInterest(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/interest_form.html', context)


def deleteInterest(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        return redirect('account')

    context = {'object': skill}
    return render(request, 'delete_template.html', context)

def projectUpdate(request, id):
    projectUpdate = Project.objects.get(id=id)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('base/single-project.html', projectUpdate.id)

    else:
        form = ProjectForm(instance=project)

    return render(request, 'base/single-prokect.html', {'form': form})


def favourites(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

   
    profiles = Profile.objects.filter(name__icontains=search_query)
    context = {'profiles': profiles}
    return render(request, 'users/favourites.html', context)
    