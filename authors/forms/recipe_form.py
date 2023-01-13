from django import forms
from recipes.models import Recipe
from utils.django_forms import add_attr
from collections import defaultdict
from utils.django_forms import add_placeholder
from authors.validators import AuthorRecipeValidator
from django.core.exceptions import ValidationError


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._my_errors = defaultdict(list)
        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')
        add_placeholder(self.fields['title'], 'Your recipe title')
        add_placeholder(
            self.fields['description'], 
            'Description of your recipe'
        )
        add_placeholder(
            self.fields['preparation_time'], 
            'How long does it take'
        )
        add_placeholder(self.fields['servings'], 'The amount')
        add_placeholder(self.fields['preparation_steps'], 'Your recipe')

    class Meta:
        model = Recipe
        fields = 'title', 'description', 'preparation_time', \
            'preparation_time_unit', 'servings', 'servings_unit', \
            'preparation_steps', 'cover'
        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
            'servings_unit': forms.Select(
                choices=(
                    ('Porções', 'Porções'),
                    ('Pedaços', 'Pedaços'),
                    ('Pessoas', 'Pessoas'),
                )
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                )
            )
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        AuthorRecipeValidator(self.cleaned_data, ErrorClass=ValidationError)
        return super_clean
