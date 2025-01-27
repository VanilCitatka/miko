from django import forms 

class ItemForm(forms.Form):
    name = forms.CharField(max_length=20, label='Название')
    price = forms.IntegerField(label='Цена')
    amount = forms.IntegerField(label='Кол-во')