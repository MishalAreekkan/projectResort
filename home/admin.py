from django.contrib import admin
# from . models import User_signin
from . models import StayPics,DinePics,User

# from django.contrib.gis.admin import OSMGeoAdmin

# Register your models here.

admin.site.register(User)
admin.site.register(StayPics)
admin.site.register(DinePics)