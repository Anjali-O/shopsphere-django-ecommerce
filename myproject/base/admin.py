from django.contrib import admin
from .models import Products

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    model=Products
    list_display=['id','pname','pcategory']


admin.site.register(Products,ProductAdmin)