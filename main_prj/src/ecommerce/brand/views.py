import csv
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, DetailView
import io
import brand
from .models import Brand
from .utils import create_thumbnail


# @staff_member_required
# def import_brands_view(request):
#     context = {}
#
#     if request.method == 'POST':
#         csv_file = request.FILES.get('csv_file')
#
#         if not csv_file:
#             messages.error(request, "No CSV file provided")
#             return render(request, 'brands/import_brands.html', context)
#
#         # Validate file extension
#         if not csv_file.name.endswith('.csv'):
#             messages.error(request, "Invalid file format. Please upload a CSV file")
#             return render(request, 'brands/import_brands.html', context)
#
#         try:
#             # Read and decode CSV file
#             data_set = csv_file.read().decode('UTF-8')
#             io_string = io.StringIO(data_set)
#
#             # Create temporary file path
#             temp_file = f"/tmp/{csv_file.name}"
#             with open(temp_file, 'w') as f:
#                 f.write(data_set)
#
#             # Import brands
#             count = import_brands_from_csv(temp_file)
#             messages.success(request, f'Successfully imported {count} brands')
#             return redirect('brands:brand_list')
#
#         except UnicodeDecodeError:
#             messages.error(request, "File encoding error. Please use UTF-8 encoded CSV")
#         except csv.Error:
#             messages.error(request, "Invalid CSV format. Please check your file structure")
#         except Exception as e:
#             messages.error(request, f"Error importing brands: {str(e)}")
#
#     return render(request, 'brands/import_brands.html', context)


class BrandListView(ListView):
    model = Brand
    template_name = 'brand/brand_list.html'
    context_object_name = 'brands'

    def get_queryset(self):
        return Brand.objects.filter(featured=True).order_by('name')


class BrandDetailView(DetailView):
    model = Brand
    template_name = 'brand/brand_detail.html'
    context_object_name = 'brand'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        brand = self.object
        context['meta_title'] = f"{brand.name} | Our Brands"
        context['meta_description'] = brand.description[:160]
        return context



def upload_logo(request):
    if request.method == 'POST':
        logo = request.FILES['logo']
        thumbnail = create_thumbnail(logo)
        brand.logo_thumbnail.save(thumbnail.name, thumbnail)