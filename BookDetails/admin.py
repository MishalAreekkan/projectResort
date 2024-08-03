from django.contrib import admin
from .models import BedField,BookData
# Register your models here.

admin.site.register(BookData)
admin.site.register(BedField)
