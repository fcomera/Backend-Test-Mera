from django import forms

class CreateMenuOptionForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField()
