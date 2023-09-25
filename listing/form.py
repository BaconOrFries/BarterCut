from django import forms
from .models import *

FORM_CLASS = 'w-full px-6 py-4 rounded-xl border'

class CreateListingForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('category', 'name', 'description', 'point', 'image')

        widgets = {
            'category': forms.Select(attrs={
                'class': FORM_CLASS
            }),
            'name': forms.TextInput(attrs={
                'class': FORM_CLASS
            }),
            'description': forms.Textarea(attrs={
                'class': FORM_CLASS
            }),
            'point': forms.TextInput(attrs={
                'class': FORM_CLASS
            }),
            'image': forms.FileInput(attrs={
                'class': FORM_CLASS
            }),
        }

class EditListingForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'description', 'point', 'image', 'is_sold')

        widgets = {
            'name': forms.TextInput(attrs={
                'class': FORM_CLASS
            }),
            'description': forms.Textarea(attrs={
                'class': FORM_CLASS
            }),
            'point': forms.TextInput(attrs={
                'class': FORM_CLASS
            }),
            'image': forms.FileInput(attrs={
                'class': FORM_CLASS
            }),
        }