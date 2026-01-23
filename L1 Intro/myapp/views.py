from django.http import HttpRequest
from django.shortcuts import render


def hello_world(request: HttpRequest):
    context = {'method': request.method}
    if request.method == 'POST':
        print(request.POST)
        context['name'] = request.POST['name']

    return render(request, 'hello_world.html', context=context)