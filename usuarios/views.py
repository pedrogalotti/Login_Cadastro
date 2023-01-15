from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants
from .models import Usuario
from hashlib import sha256


def cadastro(request):
    
    if request.session.get('usuario'):
        return redirect('/home/')

    if request.method == 'GET':
        return render(request, 'cadastro.html')
    elif request.method == 'POST':

        nome = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
    
        usuario = Usuario.objects.filter(email = email)

        if len(nome.strip()) == 0 or len(email.strip()) == 0 or len(senha.strip()) == 0 or len(confirmar_senha.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Campos inválidos')
            return redirect('/auth/cadastro/')
        
        if len(senha) < 8:
            messages.add_message(request, constants.ERROR, 'Senha menor que 8 digitos')
            return redirect('/auth/cadastro/')
        
        if senha != confirmar_senha:
            messages.add_message(request, constants.ERROR, 'Senhas diferentes')
            return redirect('/auth/cadastro/')

        if len(usuario) > 0:
            messages.add_message(request, constants.ERROR, 'Usuário já existe')
            return redirect('/auth/cadastro/')

        try:
            senha = sha256(senha.encode()).hexdigest()
            user = Usuario(
                nome=nome,
                email=email,
                senha=senha
            )

            user.save()

            messages.add_message(request, constants.SUCCESS, 'Conta cadastrada com sucesso')
            return redirect('/auth/cadastro/')
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            return redirect('/auth/cadastro/')

def login(request):

    if request.session.get('usuario'):
        return redirect('/home/')
  
    if request.method == 'GET':
        required = request.GET.get('required')  
        return render(request, 'login.html', {'required': required})

    elif request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        senha = sha256(senha.encode()).hexdigest()
        
        usuario = Usuario.objects.filter(email = email).filter(senha = senha)

        if len(email.strip()) == 0 or len(senha.strip()) == 0:
            messages.error(request, 'Campos inválidos')
            return redirect('/auth/login/')

        if len(usuario) == 0:
            messages.error(request, 'Usuário não existe. Por sorte já redirecionamos você para a página de cadastro')
            return redirect('/auth/cadastro/')
        elif len(usuario) > 0:
            request.session['usuario'] = usuario[0].id
            return redirect('/home/')

def sair(request):
    request.session.flush()
    return redirect('/auth/login/?required=3')