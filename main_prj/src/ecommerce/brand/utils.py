import os
import unicodedata
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.utils.safestring import mark_safe
from PIL import Image, ImageOps
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import re


# Slug Generation Utilities
def unique_slug_generator(instance, new_slug=None, source_field='name', max_length=50):
    """
    Generates a unique slug for model instances.
    Usage:
    class Brand(models.Model):
        def save(self, *args, **kwargs):
            if not self.slug:
                self.slug = unique_slug_generator(self)
            super().save(*args, **kwargs)
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(getattr(instance, source_field))[:max_length]

    Klass = instance.__class__
    slug = slugify(slug)[:max_length]
    qs_exists = Klass.objects.filter(slug=slug).exists()

    if qs_exists:
        new_slug = f"{slug}-{Klass.objects.all().count() + 1}"
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def ascii_slugify(value):
    """Convert unicode characters to ASCII for slug generation"""
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    return slugify(value)


# Image Processing Utilities
def validate_image_dimensions(image, min_width=100, min_height=100):
    """Validate minimum image dimensions"""
    width, height = get_image_dimensions(image)
    if width < min_width or height < min_height:
        raise ValidationError(
            f'Image must be at least {min_width}x{min_height} pixels. '
            f'Uploaded image is {width}x{height}.'
        )


def optimize_image(image, size=(800, 800), quality=85):
    """
    Optimize uploaded images:
    - Resize to specified dimensions (maintains aspect ratio)
    - Convert to RGB
    - Optimize quality
    """
    img = Image.open(image)

    # Convert to RGB if necessary
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')

    # Resize while maintaining aspect ratio
    img.thumbnail(size, Image.LANCZOS)

    # Create in-memory file
    output = BytesIO()
    img.save(output, format='JPEG', quality=quality, optimize=True)
    output.seek(0)

    # Create new InMemoryUploadedFile
    return InMemoryUploadedFile(
        output,
        'ImageField',
        f"{os.path.splitext(image.name)[0]}.jpg",
        'image/jpeg',
        output.tell(),
        None
    )


def create_thumbnail(image, size=(200, 200)):
    """Create square thumbnail with white background"""
    img = Image.open(image)

    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')

    # Create white background
    thumb = Image.new('RGB', size, (255, 255, 255))
    img.thumbnail(size, Image.LANCZOS)

    # Center image on background
    thumb.paste(
        img,
        ((size[0] - img.size[0]) // 2, (size[1] - img.size[1]) // 2)
    )

    output = BytesIO()
    thumb.save(output, format='JPEG', quality=90)
    output.seek(0)

    return InMemoryUploadedFile(
        output,
        'ImageField',
        f"thumb_{os.path.basename(image.name)}",
        'image/jpeg',
        output.tell(),
        None
    )


# Validation Utilities
def validate_website_url(value):
    """Validate proper website URL format"""
    pattern = re.compile(
        r'^(https?://)?'  # http:// or https://
        r'([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6}'  # domain
        r'(:[0-9]{1,5})?'  # port
        r'(/.*)?$'  # path
    )
    if not pattern.match(value):
        raise ValidationError('Enter a valid website URL (e.g. https://example.com)')


def validate_brand_name(value):
    """Validate brand name format"""
    if not re.match(r'^[a-zA-Z0-9\s\-&]+$', value):
        raise ValidationError(
            'Brand name can only contain letters, numbers, spaces, hyphens, and ampersands'
        )


# Template Utilities
def brand_logo_preview(brand):
    """Generate HTML for admin logo preview"""
    if brand.logo:
        return mark_safe(f'<img src="{brand.logo.url}" style="max-height: 50px;" />')
    return "No logo"


brand_logo_preview.short_description = 'Logo Preview'


# # Data Import Utilities
# def import_brands_from_csv(file_path):
#     """Batch import brands from CSV file"""
#     import csv
#     from .models import Brand
#
#     created_count = 0
#     with open(file_path, 'r') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             # Create brand if doesn't exist
#             brand, created = Brand.objects.get_or_create(
#                 name=row['name'],
#                 defaults={
#                     'description': row.get('description', ''),
#                     'website': row.get('website', '')
#                 }
#             )
#             if created:
#                 created_count += 1
#     return created_count
#
#
# def import_brands_from_csv(file_path):
#     """Batch import brands from CSV file"""
#     import csv
#     from .models import Brand
#
#     created_count = 0
#     with open(file_path, 'r', encoding='utf-8') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             # Handle boolean field
#             featured = row.get('featured', 'false').lower() == 'true'
#
#             # Create brand if doesn't exist
#             brand, created = Brand.objects.get_or_create(
#                 name=row['name'],
#                 defaults={
#                     'description': row.get('description', ''),
#                     'website': row.get('website', ''),
#                     'featured': featured
#                 }
#             )
#             if created:
#                 created_count += 1
#     return created_count