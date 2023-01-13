from collections import defaultdict
from django.core.exceptions import ValidationError
from utils.strings import is_positive_number
from recipes.models import Recipe


class AuthorRecipeValidator:
    def __init__(self, data, errors=None, ErrorClass=None):
        self.errors = defaultdict(list) if errors is None else errors
        self.ErrorClass = ValidationError if ErrorClass is None else ErrorClass
        self.data = data
        self.clean()

    def clean(self, *args, **kwargs):
        self.clean_title()
        self.clean_servings()
        self.clean_preparation_time()

        cd = self.data
        title = cd.get('title')
        description = cd.get('description')
        if title == description:
            self.errors['title'].append('Cannot be equal to description')
            self.errors['description'].append('Cannot be equal to title')

        if self.errors:
            raise ValidationError(self.errors)

    def clean_title(self):
        print(self.data)
        title = self.data.get('title')
        if len(title) < 5:
            self.errors['title'].append(
                'Title must have at least 5 characters.'
                )

        recipe_from_db = Recipe.objects.filter(
            title__iexact=title
        ).first()

        if recipe_from_db:
            self.errors['title'].append(
                'Found recipes with the same title'
            )

        return title

    def clean_preparation_time(self):
        field_name = 'preparation_time'
        field_value = self.data.get(field_name)
        if not is_positive_number(field_value):
            self.errors[field_name].append('Must be a positive number')

        return field_value

    def clean_servings(self):
        field_name = 'servings'
        field_value = self.data.get(field_name)
        if not is_positive_number(field_value):
            self.errors[field_name].append('Must be a positive number')

        return field_value
