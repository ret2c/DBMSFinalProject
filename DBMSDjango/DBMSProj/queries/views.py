from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
import mariadb

def index(request):
    return render(request, 'index.html')
