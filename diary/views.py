from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime, timedelta
from calendar import monthrange
from django.contrib import messages
import json

from .models import Transaction, Category, Goal
from .forms import TransactionForm, CategoryForm, GoalForm, UserProfileForm


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
    return redirect('diary:dashboard')


@login_required
def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
    transaction.delete()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    return redirect('diary:dashboard')


@login_required
def edit_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('diary:dashboard')
    else:
        form = TransactionForm(instance=transaction, user=request.user)
    return render(request, 'diary/edit_transaction.html', {
        'form': form,
        'transaction': transaction
    })


@login_required
def reports(request):
    return render(request, 'diary/reports.html')


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

    for category in Category.objects.filter(user=request.user):
        total = Transaction.objects.filter(
            user=request.user,
            category=category,
            transaction_type='expense'
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        if total > 0:
            data['category_data'].append({'category': category.name, 'amount': float(total)})

    return JsonResponse(data)


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
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('diary:profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'diary/profile.html', {'form': form})


# ==== METAS FINANCEIRAS ====

@login_required
def goal_list(request):
    status = request.GET.get('status', 'todas')
    goals = Goal.objects.filter(user=request.user)

    if status == 'pendentes':
        goals = goals.filter(achieved=False)
    elif status == 'concluidas':
        goals = goals.filter(achieved=True)

    return render(request, 'diary/goal_list.html', {
        'goals': goals,
        'selected_status': status,
    })


@login_required
def add_goal(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            messages.success(request, 'Meta adicionada com sucesso!')
            return redirect('diary:goal_list')
    else:
        form = GoalForm()
    return render(request, 'diary/goal_form.html', {'form': form, 'title': 'Nova Meta'})


@login_required
def edit_goal(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Meta atualizada com sucesso!')
            return redirect('diary:goal_list')
    else:
        form = GoalForm(instance=goal)
    return render(request, 'diary/goal_form.html', {'form': form, 'title': 'Editar Meta'})


@login_required
def toggle_goal_status(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    if request.method == 'POST':
        goal.achieved = not goal.achieved
        goal.save()
    return redirect('diary:goal_list')
