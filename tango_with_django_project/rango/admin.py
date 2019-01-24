from django.contrib import admin
from rango.models import Category, Page

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')

# Customises admin interface
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Page, PageAdmin)

# Update registration to include customised interface
admin.site.register(Category, CategoryAdmin)
