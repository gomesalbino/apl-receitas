import email
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import auth, messages

from receitas.models import Receita

def cadastro(request):
    """Cadastra uma nova pessoa no sistema """
    if request.method == "POST":
        nome = request.POST["nome"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
    
        if campo_vazio(nome):
            messages.error(request, "Campo nome não pode ficar em branco!")
            return redirect('cadastro')

        if campo_vazio(email):
            messages.error(request, "Campo email não pode ficar em branco!")
            return redirect('cadastro')

        if senhas_nao_sao_iguais(password, password2):
            messages.error(request, "Senhas não são iguais!")
            return redirect('cadastro')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Usuario já cadastrado!")
            return redirect('cadastro')

        if User.objects.filter(username=nome).exists():
            messages.error(request, "Usuario já cadastrado!")
            return redirect('cadastro')

        user=User.objects.create_user(username=nome, email=email, password=password)
        user.save()
        messages.success(request, "Cadastro realizado com sucesso!")
        return redirect('login')
    else:
        return render(request, 'usuarios/cadastro.html')


def login(request):
    """Realiza o login de uma pessoa no sistema """
    if request.method == "POST":
        email = request.POST["email"]
        senha = request.POST["senha"]

        if campo_vazio(email) or campo_vazio(senha):
            messages.error(request, "Email ou a senha não pode ficar branco!")
            return redirect('login')
    
        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=senha)
            if user is not None:
                auth.login(request, user)
            messages.success(request, "Login realizado com sucesso!")
            return redirect('dashboard')

    return render(request, 'usuarios/login.html')


def dashboard(request):
    """Dashboard das receitas criadas por cada usuario"""
    if request.user.is_authenticated:
        id = request.user.id
        receitas = Receita.objects.order_by('-date_receita').filter(pessoa=id)

        dados = {
            'receitas' : receitas
        }

        return render(request, 'usuarios/dashboard.html', dados)
    else:
        return redirect('index')


def logout(request):
    """Faz logout no sistema"""
    auth.logout(request)
    return redirect('index')


def campo_vazio(campo):
    """Função para verificar se o campo é vazio"""
    return not campo.strip()


def senhas_nao_sao_iguais(password, password2):
    """Valida a senha de usuario no sistema"""
    return password != password2

def handler404(request, exception):
    return render(request, 'receitas/naoencontrado.html')


