"""
URL configuration for billing project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from website import views as wb

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', wb.home, name='home'),
    
    # LOGIN & REGISTER
    path('register/', wb.register, name='register'),
    path('save_user/', wb.save_user, name='save_user'),
    path('login/', wb.login, name='login'),
    path('user_login/', wb.user_login, name='user_login'),
    path('logout/', wb.logout, name='logout'),

    # PARTY
    path('party/', wb.party, name='party'),
    path('save_party/', wb.save_party, name='save_party'),
    path('edit_party/', wb.edit_party, name='edit_party'),
    path('save_edited_party/', wb.save_edited_party, name='save_edited_party'),
    path('delete_party/', wb.delete_party, name='delete_party'),

    # OWNER
    path('owner/', wb.owner, name='owner'),
    path('save_owner/', wb.save_owner, name='save_owner'),
    path('edit_owner/', wb.edit_owner, name='edit_owner'),
    path('save_edited_owner/', wb.save_edited_owner, name='save_edited_owner'),
    path('delete_owner/', wb.delete_owner, name='delete_owner'),

    # VEHICLE
    path('vehicle/', wb.vehicle, name='vehicle'),
    path('save_vehicle_type/', wb.save_vehicle_type, name='save_vehicle_type'),
    path('save_vehicle/', wb.save_vehicle, name='save_vehicle'),
    path('edit_vehicle/', wb.edit_vehicle, name='edit_vehicle'),
    path('save_edited_vehicle/', wb.save_edited_vehicle, name='edit_vehicle'),
    path('delete_vehicle/', wb.delete_vehicle, name='delete_vehicle'),
    path('get_all_vehicle/', wb.get_all_vehicle, name='get_all_vehicle'),

    # BOOKING
    path('booking/', wb.booking, name='booking'),
    path('save_booking/', wb.save_booking, name='save_booking'),
    path('edit_booking/', wb.edit_booking, name='edit_booking'),
    path('save_edited_booking/', wb.save_edited_booking, name='save_edited_booking'),
    path('delete_booking/', wb.delete_booking, name='delete_booking'),


    # STATE and CITYS
    path('add_city/', wb.add_city, name='add_city'),
    path('save_state/', wb.save_state, name='save_state'),
    path('save_city/', wb.save_city, name='save_city'),
    path('get_all_city/', wb.get_all_city, name='get_all_city'),

    # GET PREVIOUS AMOUNT FROM PARTY
    path('get_previous_amount/', wb.get_previous_amount, name='get_previous_amount'),

    # GET BALANCE AMOUNT FROM VEHICLE OWNER
    path('get_previous_amount_to_send_vehicle_owner/',wb.get_previous_amount_to_send_vehicle_owner, name='get_previous_amount_to_send_vehicle_owner'),

    # PAYMENT RECIVED
    path('payment_recived/', wb.payment_recived, name='payment_recived'),
    path('save_payment_recived/', wb.save_payment_recived, name='save_payment_recived'),
    path('delete_payment_recived/',wb.delete_payment_recived, name='delete_payment_recived'),

    # PAYMENT SENT
    path('payment_sent/', wb.payment_sent, name='payment_sent'),
    path('save_payment_sent/', wb.save_payment_sent, name='save_payment_sent'),
    path('delete_payment_sent/', wb.delete_payment_sent, name='delete_payment_sent'),


    # ALERT
    path('alert_recive/', wb.alert_payment_pending_by_party, name='alert_payment_pending_by_party'),
    path('alert_send/', wb.alert_payment_send_to_vehicle, name='alert_payment_send_to_vehicle'),


    # DOWNLOAD PARTY EXCEL
    path('download_party_excel/', wb.download_party_excel, name='download_party_excel'),
]