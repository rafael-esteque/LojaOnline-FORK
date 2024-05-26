from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Categoria, Produto, Venda, MovimentacaoEstoque, Oferta, AtualizacaoEstoque
from .forms import ProdutoForm, MovimentacaoEstoqueForm, AtualizacaoEstoqueForm


def pagina_inicial(request):
    return render(request, 'pagina_inicial.html')


def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'lista_categorias.html', {'categorias': categorias})


def detalhes_categoria(request, categoria_id):
    categoria = Categoria.objects.get(id=categoria_id)
    return render(request, 'detalhes_categoria.html', {'categoria': categoria})


def lista_produtos(request):
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        produtos = Produto.objects.filter(categoria_id=categoria_id)
    else:
        produtos = Produto.objects.all()
    categorias = Categoria.objects.all()
    return render(request, 'lista_produtos.html', {'produtos': produtos, 'categorias': categorias})


def detalhes_produto(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    return render(request, 'detalhes_produto.html', {'produto': produto})


def remover_produto(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    if request.method == 'POST':
        produto.delete()
        return redirect('lista_produtos')
    return render(request, 'remover_produto.html', {'produto': produto})


def relatorio_estoque(request):
    produtos = Produto.objects.all()
    return render(request, 'relatorio_estoque.html', {'produtos': produtos})


def historico_vendas(request):
    vendas = Venda.objects.all()
    return render(request, 'historico_vendas.html', {'vendas': vendas})


def lista_movimentacoes(request):
    movimentacoes = MovimentacaoEstoque.objects.all()
    return render(request, 'lista_movimentacoes.html', {'movimentacoes': movimentacoes})


def detalhes_movimentacao(request, movimentacao_id):
    movimentacao = MovimentacaoEstoque.objects.get(id=movimentacao_id)
    return render(request, 'detalhes_movimentacao.html', {'movimentacao': movimentacao})


def adicionar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'adicionar_produto.html', {'form': form})


def adicionar_movimentacao(request):
    if request.method == 'POST':
        form = MovimentacaoEstoqueForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_movimentacoes')
    else:
        form = MovimentacaoEstoqueForm()
    return render(request, 'adicionar_movimentacao.html', {'form': form})


def salvar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a success page or another URL
            return redirect('pagina_sucesso')
    else:
        form = ProdutoForm()
    return render(request, 'salvar_produto.html', {'form': form})


def salvar_movimentacao(request):
    if request.method == 'POST':
        form = MovimentacaoEstoqueForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pagina_sucesso_movimentacao')
    else:
        form = MovimentacaoEstoqueForm()
    return render(request, 'salvar_movimentacao.html', {'form': form})


def detalhes_oferta(request, oferta_id):
    oferta = get_object_or_404(Oferta, pk=oferta_id)
    return render(request, 'detalhes_oferta.html', {'oferta': oferta})


def remover_oferta(request, oferta_id):
    oferta = get_object_or_404(Oferta, pk=oferta_id)
    if request.method == 'POST':
        oferta.delete()
        return redirect('lista_ofertas')
    return render(request, 'remover_oferta.html', {'oferta': oferta})

def atualizar_estoque(request):
    if request.method == 'POST':
        form = AtualizacaoEstoqueForm(request.POST)
        if form.is_valid():
            atualizacao = form.save()
            produto = atualizacao.produto
            produto.estoque += atualizacao.quantidade
            produto.save()
            messages.success(request, f'Estoque de {produto.nome} atualizado com sucesso!')
            return redirect('pagina_inicial')
    else:
        form = AtualizacaoEstoqueForm()
    return render(request, 'atualizar_estoque.html', {'form': form})
