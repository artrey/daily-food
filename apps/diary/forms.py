from django import forms

from . import models


class EatingActionCreateForm(forms.ModelForm):
    class Meta:
        model = models.EatingAction
        exclude = 'user',
