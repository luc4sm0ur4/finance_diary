from django import forms
from .models import Transaction, Category

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'description', 'date', 'category', 'transaction_type']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'amount': forms.NumberInput(attrs={
                'step': '0.01',
                'min': '0.01',
                'class': 'form-control'
            }),
            'description': forms.TextInput(attrs={
                'placeholder': 'Descrição da transação',
                'class': 'form-control'
            }),
            'transaction_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'amount': 'Valor',
            'description': 'Descrição',
            'date': 'Data',
            'category': 'Categoria',
            'transaction_type': 'Tipo',
        }

    def __init__(self, *args, **kwargs):
        # Captura o usuário passado como argumento
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filtra as categorias apenas do usuário logado
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user).order_by('name')
        
        # Torna a categoria opcional
        self.fields['category'].required = False


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'icon']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Nome da categoria',
                'class': 'form-control'
            }),
            'icon': forms.TextInput(attrs={
                'placeholder': 'Ícone (Material Icons)',
                'list': 'icon-list',  # permite usar <datalist> no template
                'class': 'form-control'
            }),
        }
        labels = {
            'name': 'Nome',
            'icon': 'Ícone',
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError('O nome da categoria é obrigatório.')
        return name
