from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from tag.models import Tag
from collections import defaultdict
from django.core.exceptions import ValidationError
import os
from django.conf import settings
from PIL import Image
# from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=65)  # verbose_name=_('Título')
    description = models.CharField(max_length=165)
    slug = models.SlugField(unique=True, blank=True)
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=65)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(upload_to='recipes/covers/%Y/%m/%d/', blank=True, default='')     # noqa: E501
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, default=None)      # Uma Categoria para varias Receitas # noqa: E501
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)     # Um Autor para varias receitas # noqa: E501
    tags = models.ManyToManyField(Tag, default='', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipes:recipe', args=(self.id,))

    @staticmethod
    def resize_image(image, new_width=840):
        image_full_path = os.path.join(settings.MEDIA_ROOT, image.name)
        image_pillow = Image.open(image_full_path)
        original_width, original_height = image_pillow.size
        if original_width < new_width:
            image_pillow.close()
            return
        new_height = round(new_width * original_height) / original_width
        new_image = image_pillow.resize((new_width, new_height), Image.LANCZOS)
        new_image.save(
            image_full_path,
            optimize=True,
            quality=50
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.title)}'
            self.slug = slug

        saved = super().save(*args, **kwargs)

        if self.cover:
            try:
                self.resize_image(self.cover, 800)
            except FileNotFoundError:
                ...

        return saved

    def clean(self, *args, **kwargs):
        error_messages = defaultdict(list)

        recipe_from_db = Recipe.objects.filter(
            title__iexact=self.title
        ).first()

        if recipe_from_db:
            if recipe_from_db.pk != self.pk:
                error_messages['title'].append(
                    'Found recipes with the same title'
                )
        if error_messages:
            raise ValidationError(error_messages)
