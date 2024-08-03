from django.urls import path
from . import views

urlpatterns = [
    path('bookField/', views.bookField, name='bookField'),
    path('booking/<int:id>/<int:year>/<int:month>/', views.booking, name='booking'),
    path('cancel_booking/<int:id>/<int:year>/<int:month>/', views.cancel_booking, name='cancel_booking'),
    path('booking_list/<int:id>/<int:year>/<int:month>/', views.booking_list, name='booking_list'),
    path('paysuccess/<int:id>/', views.payment_success, name='paysuccess'),
    path('payfailed/<int:id>/', views.payment_failed, name='payfailed'),
]
