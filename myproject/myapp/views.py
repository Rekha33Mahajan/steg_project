from django import urls
from django.shortcuts import render
from PIL import Image
import stepic

def home(request):
    return render(request, 'home.html')

def display_image(filename):
	return render(urls('static', filename='encrypted_images/' + filename), code=301)

def hide_text_in_img(image, text):
    rgb_image = image.convert('RGB')
    data = text.encode('utf-8')
    return stepic.encode(rgb_image, data)

def encrypt(request):
    message = " "
    if request.method == "POST":
        text = request.POST['text']
        image_file = request.FILES['image']
        image = Image.open(image_file)
        new_image = hide_text_in_img(image, text)
        image_path = 'encrypted_images/' + 'new_' + image_file.name
        new_image.save(image_path)
        message = "Text has been encrypted in the image"
        # return render(request, 'encrypt_result.html', {
        #      'text': text,
        # })
    return render(request, 'encrypt.html', locals())    

def extract_text_from_image(image):
    data = stepic.decode(image)
    if isinstance(data, bytes):
        return data.decode('utf-8')
    return data

def decrypt(request):
    text = " "
    extracted_image_path = None
    if request.method == 'POST':
        image_file = request.FILES['image']
        image = Image.open(image_file)
        text = extract_text_from_image(image)
    
        decrypted_image_path = 'decrypted_images/' + 'new_'+image_file.name
        image.save(decrypted_image_path)
        return render(request, 'decrypt_result.html', {
             'text': text,
        })
    return render(request, 'decrypt.html',locals())

def explore(request):
    return render(request, 'explore.html')

