from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import CreateUserForm
from django.contrib import messages
# Create your views here.
from .forms import LoginForm, DataForm

from django.shortcuts import render,HttpResponse
from .serializers import CropSerializer
from .models import Crop
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

class CropView(viewsets.ModelViewSet):
    queryset = Crop.objects.all()
    serializer_class = CropSerializer



def sign_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                # messages.success(request,f'Hi {username.title()}, welcome back!')
                return redirect('index')
        
        # form is not valid or user is not authenticated
        messages.error(request, 'Invalid username or password')
        return render(request, 'login.html', {'form': form})

    # Default response for other HTTP methods
    return render(request, 'login.html', {'form': LoginForm()})
def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'user account succesful created')
            return redirect('login')
            
        else: 
            context = {'form':form}
            return render(request, 'register.html', context)

def sign_out(request):
    logout(request)
    # messages.success(request,f'You have been logged out.')
    return redirect('login') 


def index(request):
    return render(request,'index.html')

def details(request):
    if request.method == 'POST':
        form = DataForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('results')
    else:
        form = DataForm()
    context ={
        'form' : form
    }
    return render(request,'details.html', context)

def results(request):
    predicted_crop = Crop.objects.all()
    context = {
        'predicted_crop': predicted_crop
    }
    return render(request, 'results.html', context)