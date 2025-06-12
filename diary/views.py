### ARQUIVO: views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime, timedelta
from calendar import monthrange
from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm
import json

from .models import Transaction, Category
from .forms import TransactionForm, CategoryForm

@login_required
def dashboard(request):
    today = timezone.now().date()
    first_day_of_month = today.replace(day=1)

    transactions = Transaction.objects.filter(
        user=request.user,
        date__gte=first_day_of_month,
        date__lte=today
    ).order_by('-date')

    income_sum = transactions.filter(transaction_type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    expense_sum = transactions.filter(transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = income_sum - expense_sum

    expense_by_category = []
    categories = Category.objects.filter(user=request.user)
    for category in categories:
        total = transactions.filter(category=category, transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
        if total > 0:
            expense_by_category.append({
                'category': category.name,
                'icon': category.icon,
                'amount': float(total)
            })

    context = {
        'transactions': transactions[:10],
        'income_sum': income_sum,
        'expense_sum': expense_sum,
        'balance': balance,
        'expense_by_category': json.dumps(expense_by_category),
        'categories': categories,
        'transaction_form': TransactionForm(user=request.user),
        'category_form': CategoryForm(),
        'today': today
    }

    return render(request, 'diary/dashboard.html', context)

@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success'})

            return redirect('diary:dashboard')  # <- corrigido
    return redirect('diary:dashboard')  # <- corrigido

@login_required
def delete_transaction(request, transaction_id):
    try:
        transaction = Transaction.objects.get(id=transaction_id, user=request.user)
        transaction.delete()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})

        messages.success(request, 'Transação excluída com sucesso.')
    except Transaction.DoesNotExist:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'not_found'}, status=404)
        messages.error(request, 'Transação não encontrada.')

    return redirect('diary:dashboard')

@login_required
def get_report_data(request, report_type):
    today = timezone.now().date()
    data = {
        'labels': [],
        'income': [],
        'expense': [],
        'balance': [],
        'category_data': []
    }

    def aggregate_range(start_date, end_date):
        income = Transaction.objects.filter(
            user=request.user,
            date__gte=start_date,
            date__lte=end_date,
            transaction_type='income'
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        expense = Transaction.objects.filter(
            user=request.user,
            date__gte=start_date,
            date__lte=end_date,
            transaction_type='expense'
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        return float(income), float(expense)

    if report_type == 'monthly':
        start_date = today.replace(day=1)
        for i in range(1, today.day + 1):
            current = start_date.replace(day=i)
            income, expense = aggregate_range(current, current)
            data['labels'].append(current.strftime('%d/%m'))
            data['income'].append(income)
            data['expense'].append(expense)
            data['balance'].append(income - expense)

        category_totals = []
        for category in Category.objects.filter(user=request.user):
            total = Transaction.objects.filter(
                user=request.user,
                category=category,
                transaction_type='expense',
                date__gte=start_date,
                date__lte=today
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            if total > 0:
                category_totals.append({'category': category.name, 'amount': float(total)})
        data['category_data'] = category_totals

    elif report_type in ['quarterly', 'yearly']:
        months = 3 if report_type == 'quarterly' else 12
        for i in reversed(range(months)):
            month = today.month - i
            year = today.year
            if month <= 0:
                month += 12
                year -= 1
            start = datetime(year, month, 1).date()
            end = datetime(year, month, monthrange(year, month)[1]).date()
            income, expense = aggregate_range(start, end)
            data['labels'].append(start.strftime('%b/%y'))
            data['income'].append(income)
            data['expense'].append(expense)
            data['balance'].append(income - expense)

        category_totals = []
        period_start = today - timedelta(days=90 if report_type == 'quarterly' else 365)
        for category in Category.objects.filter(user=request.user):
            total = Transaction.objects.filter(
                user=request.user,
                category=category,
                transaction_type='expense',
                date__gte=period_start,
                date__lte=today
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            if total > 0:
                category_totals.append({'category': category.name, 'amount': float(total)})
        data['category_data'] = category_totals

    return JsonResponse(data)

@login_required
def reports(request):
    return render(request, 'diary/reports.html')

@login_required
def category_list(request):
    categories = Category.objects.filter(user=request.user).order_by('name')
    return render(request, 'diary/category_list.html', {'categories': categories})

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, 'Categoria adicionada com sucesso!')
            return redirect('diary:category_list')
    else:
        form = CategoryForm()
    return render(request, 'diary/category_form.html', {'form': form, 'title': 'Nova Categoria'})

@login_required
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria atualizada com sucesso!')
            return redirect('diary:category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'diary/category_form.html', {'form': form, 'title': 'Editar Categoria'})

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'diary/profile.html', {'form': form})
