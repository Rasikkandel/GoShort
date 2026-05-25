from django.shortcuts import render
from django.http import HttpResponse 

dict = {} 
def base62(num): 
    if num == 0:
        return BASE62[0]

    result = []
    while num > 0:
        remainder = num % 62
        result.append(BASE62[remainder])
        num //= 62

    return ''.join(reversed(result))
# Create your views here.
def makeshort(request , long_url) : 
    return HttpResponse(base62(long_url)) 
