from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('add-balance/', views.add_balance, name='add_balance'),
    path('balance/', views.balance, name='balance'),
    path('send-notifications/', views.send_payment_notifications, name='send_notifications'),
    path('pay-notification/<int:notification_id>/', views.pay_notification, name='pay_notification'),
    path('notifications-sent/', views.notifications_sent_view, name='notifications_sent'),

]
