from typing import Text
from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpRequest
from topspell.Corrector import Corrector
# Create your views here.

Cor = Corrector()

def he(request):
    data = request.POST.get('text')
    if data != None:
        ans=list_of_possible_spellings(text=data)
        if len(data.split())>1:
            return render(request,'index.html',{'data': data if data is None else ans[1],'answer':' '.join(ans[0])})
        else:
            return render(request,'index.html',{'data': data if data is None else ans[1],'answer':ans[0]})
    else:
        return render(request,'index.html',{'data': data})

def list_of_possible_spellings(text):
    
    if len(text.split()) > 1: 
        return Cor.sensitive_corrector(text)
    else:
        return Cor.corrector(text)
