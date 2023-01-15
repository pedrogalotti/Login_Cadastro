from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def about(request):
    return render(request, 'about.html')
 

def home(request):
    if request.session.get('usuario'):

        return render(request, 'home.html', {'usuario_logado': request.session.get('usuario')})
    else:
        return redirect('/auth/login/?required=1')