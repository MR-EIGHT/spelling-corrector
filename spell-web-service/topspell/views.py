from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpRequest
from topspell.Corrector import Corrector
# Create your views here.


def he(request):
    data = request.POST.get('text')
    print(data)
    return render(request,'index.html',{'data': data if data is None else list_of_possible_spellings(text=data)})

def list_of_possible_spellings(text):
    Cor = Corrector()
    print(len(text.split()))
    if len(text.split()) > 1: 
        return Cor.sensitive_corrector(text)
    else:
        return Cor.corrector(text)
