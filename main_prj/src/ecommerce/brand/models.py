from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django import forms
from brand.utils import validate_brand_name, validate_website_url


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    logo = models.ImageField(upload_to='brands/logos/')
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Brands"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('brands:brand_detail', args=[self.slug])


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'

    def clean_name(self):
        name = self.cleaned_data['name']
        validate_brand_name(name)
        return name

    def clean_website(self):
        website = self.cleaned_data['website']
        validate_website_url(website)
        return website


