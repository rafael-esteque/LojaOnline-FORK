from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

    
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    quantidade = models.PositiveIntegerField(default=0)
    unidade_medida = models.CharField(max_length=50, default='')
    codigo_barras = models.CharField(max_length=100, default='')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class Pedido(models.Model):
    cliente = models.CharField(max_length=100)
    produtos = models.ManyToManyField(Produto, through='ItemPedido')

    def __str__(self):
        return self.nome


class ItemPedido(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    quantidade = models.IntegerField()

    def __str__(self):
        return self.nome

    
class Venda(models.Model):
    produto = models.ForeignKey('Produto', on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    data_venda = models.DateTimeField(auto_now_add=True)
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)
    cliente = models.CharField(max_length=100, blank=True, null=True)
    metodo_pagamento = models.CharField(max_length=50, blank=True, null=True)
    preco_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):

        self.subtotal = self.quantidade * self.preco_unitario
        
        if not self.preco_total:
            self.preco_total = self.subtotal
        
        super().save(*args, **kwargs)
        
        self.produto.estoque -= self.quantidade
        self.produto.save()

    def __str__(self):
        return f"Venda de {self.quantidade} unidades de {self.produto.nome} em {self.data_venda}"
    

class MovimentacaoEstoque(models.Model):
    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    ]
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    tipo_movimentacao = models.CharField(max_length=10, choices=TIPO_CHOICES)
    quantidade = models.IntegerField()
    data_movimentacao = models.DateTimeField(auto_now_add=True)
    usuario_responsavel = models.CharField(max_length=100)
    motivo = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.tipo_movimentacao} de {self.quantidade} unidades de {self.produto.nome} em {self.data_movimentacao}"


class Oferta(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='ofertas/')

    def __str__(self):
        return self.nome    

class AtualizacaoEstoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    data = models.DateTimeField(auto_now_add=True)
    motivo = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.produto.nome} - {self.quantidade}"    

# Create your models here.
