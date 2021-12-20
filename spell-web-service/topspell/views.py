from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpRequest
# Create your views here.


def he(request):
    data = request.POST.get('text')
    print(data)
    return render(request,'index.html',{'data': data})

def list_of_possible_spellings(text):
    return 0
