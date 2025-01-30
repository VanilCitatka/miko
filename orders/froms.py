from django import forms 

class ItemForm(forms.Form):
    name = forms.CharField(max_length=20, label='Название')
    price = forms.DecimalField(label='Цена', max_digits=10, decimal_places=2)
    amount = forms.IntegerField(label='Кол-во')