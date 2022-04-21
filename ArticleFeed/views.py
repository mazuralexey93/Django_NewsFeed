from django.shortcuts import render

def index(request):
    title = 'Mainpage'

    context = {
        'title': title,
    }

    return render(request, 'index.html', context)
