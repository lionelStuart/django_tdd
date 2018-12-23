from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.

def home_page(request):
    html = '<html><title>TO-DO</title></html>'
    return HttpResponse(html)
    pass
