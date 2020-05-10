from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def compareFaces(request):
    return HttpResponse('This should return the face of the person infront of the camera')