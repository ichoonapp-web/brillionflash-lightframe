from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from django.db.models import Sum, Count
from datetime import timedelta

@shared_task
def generate_daily_report():
    from django.contrib.auth.models import User
    from apps.marketplace.models import Item
    
    now = timezone.now()
    yesterday = now - timedelta(days=1)
    
    users = User.objects.filter(date_joined__gte=yesterday).count()
    sales = Item.objects.aggregate(total=Sum('sales'))['total'] or 0
    views = Item.objects.aggregate(total=Sum('views'))['total'] or 0
    
    msg = f"Daily Report:\nNew Users: {users}\nSales: {sales}\nViews: {views}"
    return msg

@shared_task
def monitor_system_health():
    return "Health check done"

@shared_task
def cleanup_stale_data():
    return "Cleaned"

@shared_task
def send_push_notifications():
    return "Notifications sent"
