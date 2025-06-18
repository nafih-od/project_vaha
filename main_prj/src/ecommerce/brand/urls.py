from django.template.context_processors import static
from django.urls import path

from ecommerce import settings
from . import views

app_name = 'brand'

urlpatterns = [
    path('', views.BrandListView.as_view(), name='brand_list'),
    path('<slug:slug>/', views.BrandDetailView.as_view(), name='brand_detail'),
    # Add import path
    # path('import/', views.import_brands_view, name='import_brands'),
]

