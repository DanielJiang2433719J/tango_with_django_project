from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context_dict = {'boldmessage': "Crunchy, creamy, cookie,\
     candy, cupcake!"}
    return render(request, 'rango/index.html', context=context_dict)
#    return HttpResponse("<a href = '/rango/about'> About </a>")

def about(request):
    about_dict = {}
    return render(request, 'rango/about.html', context=about_dict)
#    return HttpResponse("Rango says here is the about page.\
#    <br> <a href = '/rango'> Back home </a>")
