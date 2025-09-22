from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from .models import LoginHistory
from django.utils import timezone
import json
from datetime import datetime
from django.contrib.auth.models import User

def home(request):
    return render(request, 'home.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                LoginHistory.objects.create(user=user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    last_login = LoginHistory.objects.filter(user=request.user, logout_timestamp__isnull=True).order_by('-login_timestamp').first()
    if last_login:
        last_login.logout_timestamp = timezone.now()
        last_login.save()
    logout(request)
    return redirect('home')

@login_required
def dashboard_view(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')

    selected_date_str = request.GET.get('date')
    is_daily_view = bool(selected_date_str)
    all_user_logins = LoginHistory.objects.filter(user=request.user).order_by('-login_timestamp')

    if is_daily_view:
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
        login_history = all_user_logins.filter(login_timestamp__date=selected_date)
        total_logins_today = login_history.count()
        stats_title = "Logins on Date"
        total_logins_stat = total_logins_today
        selected_date_formatted = selected_date.strftime('%B %d, %Y')
    else:
        login_history = all_user_logins[:20]
        total_logins_today = all_user_logins.count()
        stats_title = "Total Logins (All Time)"
        total_logins_stat = total_logins_today
        selected_date_formatted = "all time"
        selected_date_str = ""

    time_of_day_counts = {"Morning": 0, "Afternoon": 0, "Evening": 0, "Night": 0}
    for login_record in all_user_logins:
        hour = timezone.localtime(login_record.login_timestamp).hour
        if 5 <= hour < 12: time_of_day_counts["Morning"] += 1
        elif 12 <= hour < 17: time_of_day_counts["Afternoon"] += 1
        elif 17 <= hour < 21: time_of_day_counts["Evening"] += 1
        else: time_of_day_counts["Night"] += 1
    
    context = {
        'total_logins': total_logins_stat,
        'stats_title': stats_title,
        'login_history': login_history,
        'total_logins_today': total_logins_today,
        'selected_date_str': selected_date_str,
        'selected_date_formatted': selected_date_formatted,
        'is_daily_view': is_daily_view,
        'chart_labels': json.dumps(list(time_of_day_counts.keys())),
        'chart_data': json.dumps(list(time_of_day_counts.values())),
    }
    return render(request, 'dashboard.html', context)

@login_required
def admin_dashboard_view(request):
    if not request.user.is_staff:
        return redirect('dashboard')
    
    normal_users = User.objects.filter(is_staff=False)
    
    users_with_chart_data = []
    
    for user in normal_users:
        all_user_logins = LoginHistory.objects.filter(user=user)
        
        time_of_day_counts = {"Morning": 0, "Afternoon": 0, "Evening": 0, "Night": 0}
        for login_record in all_user_logins:
            hour = timezone.localtime(login_record.login_timestamp).hour
            if 5 <= hour < 12: time_of_day_counts["Morning"] += 1
            elif 12 <= hour < 17: time_of_day_counts["Afternoon"] += 1
            elif 17 <= hour < 21: time_of_day_counts["Evening"] += 1
            else: time_of_day_counts["Night"] += 1
        
        users_with_chart_data.append({
            'user_info': user,
            'chart_labels': json.dumps(list(time_of_day_counts.keys())),
            'chart_data': json.dumps(list(time_of_day_counts.values())),
        })
        
    return render(request, 'admin_dashboard.html', {'users_data': users_with_chart_data})

@login_required
def user_login_history_view(request, user_id):
    if not request.user.is_staff:
        return redirect('dashboard')

    user = get_object_or_404(User, id=user_id)
    login_history = LoginHistory.objects.filter(user=user).order_by('-login_timestamp')
    
    context = {
        'user': user,
        'login_history': login_history,
    }
    return render(request, 'user_login_history.html', context)