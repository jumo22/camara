from django import forms


class SearchForm(forms.Form):
    keyword = forms.CharField(label='Search word', max_length=20)