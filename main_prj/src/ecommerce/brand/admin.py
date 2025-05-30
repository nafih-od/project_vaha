from django.contrib import admin
from .models import Brand


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'featured', 'created_at')
    list_filter = ('featured', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {'fields': ('name', 'slug', 'featured')}),
        ('Media', {'fields': ('logo',)}),
        ('Content', {'fields': ('description', 'website')}),
        ('Metadata', {'fields': ('created_at', 'updated_at')}),
    )


from .utils import brand_logo_preview, validate_website_url, validate_brand_name


# @admin.register(Brand)
# class BrandAdmin(admin.ModelAdmin):
#     list_display = ('name', 'slug', 'featured', brand_logo_preview, 'created_at')
#
#     # ... existing config ...
#
#     # Add custom form validation
#     def formfield_for_dbfield(self, db_field, **kwargs):
#         field = super().formfield_for_dbfield(db_field, **kwargs)
#         if db_field.name == 'website':
#             field.validators.append(validate_website_url)
#         if db_field.name == 'name':
#             field.validators.append(validate_brand_name)
#         return field