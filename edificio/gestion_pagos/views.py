from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import BalanceForm
from django.contrib.admin.views.decorators import staff_member_required
from .models import PaymentNotification, CustomUser
from django.shortcuts import get_object_or_404


# PAGINA DEL INICIO
def home(request):
    return HttpResponse("¡Bienvenido al sistema de gestión de pagos del edificio!")

# REGISTRO DEL USUARIO 
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  
            user.save()
            login(request, user)  
            return redirect('home')  
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})



@login_required
def add_balance(request):
    if request.method == 'POST':
        form = BalanceForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            request.user.balance += amount  
            request.user.save()
            return redirect('balance') 
    else:
        form = BalanceForm()
    return render(request, 'add_balance.html', {'form': form})




@login_required
def balance(request):
    return render(request, 'balance.html', {'balance': request.user.balance})



@staff_member_required
def send_payment_notifications(request):
    if request.method == 'POST':
        amount_due = request.POST.get('amount_due')
        if amount_due:
            users = CustomUser.objects.filter(is_staff=False)  
            for user in users:
                PaymentNotification.objects.create(user=user, amount_due=amount_due)
            return redirect('notifications_sent') 
    return render(request, 'send_notifications.html')



@login_required
def pay_notification(request, notification_id):
    notification = get_object_or_404(PaymentNotification, id=notification_id, user=request.user)
    if not notification.paid:
        if request.user.balance >= notification.amount_due:
            request.user.balance -= notification.amount_due
            request.user.save()
            notification.paid = True
            notification.save()
            return redirect('balance')
        else:
            return render(request, 'payment_failed.html', {'notification': notification})
    return redirect('balance')



def notifications_sent_view(request):
    return render(request, 'gestion_pagos/notifications_sent.html')







