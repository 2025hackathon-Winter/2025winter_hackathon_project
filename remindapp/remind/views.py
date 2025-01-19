from django.shortcuts import render
from pathlib import Path
from django.http import HttpResponse
from django.views.generic import TemplateView

def helloworldfunction(reqest):
    returnedobject = HttpResponse('<h1>hello world</h1>')
    return returnedobject

class HelloWorldClass(TemplateView):
    template_name = 'base.html'