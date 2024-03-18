# views.py

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from email.mime import image
from threading import local
from httpx import post
from numpy import extract
import stepic
from PIL import Image

def index(request):
    return render(request, 'index.html')

def hide_text_in_img(image, text):
    rgb_image = image.convert('RGB')
    data = text.encode('utf-8')
    return stepic.encode(rgb_image, data)

def encryption_view(request):
    message = " "
    if request.method == "POST":
        text = request.POST['text']
        image_file = request.FILES['image']
        image = Image.open(image_file)
        new_image = hide_text_in_img(image, text)
        image_path = 'encrypted_images/' + 'new_' + image_file.name
        new_image.save(image_path)
        message = "Text has been encrypted in the image"
    return render(request, 'encryption.html', locals())

def extract_text_from_image(image):
    data = stepic.decode(image)
    if isinstance(data, bytes):
        return data.decode('utf-8')
    return data

def decryption_view(request):
    text = " "
    extracted_image_path = None
    if request.method == 'POST':
        image_file = request.FILES['image']
        image = Image.open(image_file)
        text = extract_text_from_image(image)
    
        decrypted_image_path = 'decrypted_images/' + 'new_'+image_file.name
        image.save(decrypted_image_path)
    return render(request, 'decryption.html',locals())

def about_view(request):
    return render(request, 'about.html')

def help_view(request):
    return render(request, 'help.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')  # Redirect to the home page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'auth/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('encryption')  # Redirect to the home page after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('index')  # Redirect to the home page after logout
