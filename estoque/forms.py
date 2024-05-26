from django import forms
from .models import Produto, MovimentacaoEstoque, AtualizacaoEstoque

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'preco_venda', 'preco_custo', 'quantidade', 'unidade_medida', 'codigo_barras', 'categoria']

class MovimentacaoEstoqueForm(forms.ModelForm):
    class Meta:
        model = MovimentacaoEstoque
        fields = ['produto', 'tipo_movimentacao', 'quantidade', 'usuario_responsavel', 'motivo']
        
class AtualizacaoEstoqueForm(forms.ModelForm):
    class Meta:
        model = AtualizacaoEstoque
        fields = ['produto', 'quantidade', 'motivo']
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
            'motivo': forms.Textarea(attrs={'class': 'form-control'}),
        }        