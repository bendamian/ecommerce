from django.urls import reverse
from django.db import models
from django.utils.html import format_html


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100 ,db_index=True)
    slug = models.SlugField(max_length=100 ,unique=True)

    class Meta:
    
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    

class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)
    image = models.ImageField(upload_to='images/', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def thumbnail(self):
        if self.image:
            return format_html('<img src="{}" width="60" height="60" style="object-fit:cover;" />', self.image.url)
        return ""
    thumbnail.short_description = 'Thumbnail'
