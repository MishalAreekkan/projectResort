from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('register',views.register,name='register'),
    path('login',views.user_login,name='login'),
    path('logout',views.user_logout,name='logout'),
    path('stay',views.stay,name='stay'),
    path('dine',views.dine,name='dine'),
    path('spa',views.spa,name='spa'),
    path('celebrate',views.celebrate,name='celebrate'),
    path('gallery',views.gallery,name='gallery'),
    path('offers',views.offers,name='offers'),
    path('dinepic',views.dinepic,name='dinepic'),
    path('urldate/<int:id>/',views.url_date,name='urldate'),
    path('stayedit/<int:id>/',views.stay_pic_edit,name='stayedit'),
    path('staydelete/<int:id>/',views.stay_delete,name='staydelete'),

    #  path('calendar/<int:year>/<int:month>/', calendarshow, name='calendar'),
]

