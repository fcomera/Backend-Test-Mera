from django import forms

from datetime import datetime

from menus.models.menu import Menu
from menus.models.menu_option import MenuOption

class CreateMenuForm(forms.Form):
    name = forms.CharField()
    date = forms.DateField(
        initial=datetime.now()
    )

    def save(self):
        import pdb; pdb.set_trace()
        if self.is_valid():
            instance = Menu.objects.create(
                **self.cleaned_data
            )

