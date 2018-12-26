from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from .models import Item


def home_page(request):
    if request.method == "POST":
        Item.objects.create(text=request.POST['item_text'])
        return redirect("/list/the-only-list/")


def view_list(request):
    items = Item.objects.all()
    return render(request, "list.html", {"items": items})
