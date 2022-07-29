from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib import  messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from receitas.models import Receita


def index(request):
    """Pagina principal que lista as receitas no sistema"""
    receitas = Receita.objects.order_by('-date_receita').filter(publicada=True)
    paginator = Paginator(receitas, 6)
    page = request.GET.get('page')
    receitas_por_pagina = paginator.get_page(page)

    dados = {
        'receitas': receitas_por_pagina
    }

    return render(request, 'receitas/index.html', dados)


def receita(request, receita_id):
    """Exibi id de uma receita no sistema"""
    receita = get_object_or_404(Receita, pk=receita_id)

    receita_a_exibir = {
        'receita' : receita
    }

    return render(request, 'receitas/receita.html', receita_a_exibir)


def cria_receita(request):
    """Cria uma nova receita no sistema"""
    if request.method == "POST":
        nome_receita = request.POST["nome_receita"]
        ingredientes = request.POST["ingredientes"]
        modo_preparo = request.POST["modo_preparo"]
        tempo_preparo = request.POST["tempo_preparo"]
        rendimento = request.POST["rendimento"]
        categoria = request.POST["categoria"]
        foto_receita = request.FILES["foto_receita"]
        if campo_vazio(nome_receita):
            messages.error(request, "Campo nome da receita não pode ficar vazio!")
            return redirect('cria_receita')

        if campo_vazio(ingredientes):
            messages.error(request, "Campo ingredientes não pode ficar vazio!")
            return redirect('cria_receita')

        if campo_vazio(modo_preparo):
            messages.error(request, "Campo modo preparo não pode ficar vazio!")
            return redirect('cria_receita')

        if campo_vazio(tempo_preparo):
            messages.error(request, "Campo tempo de preparo não pode ficar vazio!")
            return redirect('cria_receita')

        if campo_vazio(rendimento):
            messages.error(request, "Campo rendimento não pode ficar vazio!")
            return redirect('cria_receita')

        if campo_vazio(categoria):
            messages.error(request, "Campo categoria não pode ficar vazio!")
            return redirect('cria_receita')
      

        user = get_object_or_404(User, pk=request.user.id)
        receita = Receita.objects.create(pessoa=user, nome_receita=nome_receita, ingredientes=ingredientes, modo_preparo=modo_preparo, tempo_preparo=tempo_preparo, rendimento=rendimento, categoria=categoria, foto_receita=foto_receita)
        receita.save()
        return redirect('dashboard')
    else:
    
        return render(request, 'receitas/cria_receita.html')


def deleta_receita(request, receita_id):
    """Apaga uma receita no sistema"""
    receita = get_object_or_404(Receita, pk=receita_id)
    receita.delete()
    return redirect('dashboard')


def edita_receita(request, receita_id):
    """Edita uma receita no sistema"""
    receita = get_object_or_404(Receita, pk=receita_id)

    receita_a_editar = {
        'receita' : receita
    }
    return render(request, 'receitas/edita_receita.html', receita_a_editar)


def atualiza_receita(request):
    """Atualiza uma edição da receita no sistema"""
    if request.method == "POST":
        receita_id = request.POST["receita_id"]
        r = Receita.objects.get(pk=receita_id)
        r.nome_receita = request.POST["nome_receita"]
        r.ingredientes = request.POST["ingredientes"]
        r.modo_preparo = request.POST["modo_preparo"]
        r.tempo_preparo = request.POST["tempo_preparo"]
        r.rendimento = request.POST["rendimento"]
        r.categoria = request.POST["categoria"]
        if 'foto_receita' in request.FILES:
            r.foto_receita = request.FILES["foto_receita"]
        r.save()
        return redirect('dashboard')


def campo_vazio(campo):
    """Valida os campos em brancos"""
    return not campo.strip()

