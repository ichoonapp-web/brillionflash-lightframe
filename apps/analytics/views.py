from django.db.models import Sum, Count
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from datetime import timedelta

class AnalyticsDashboardView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        from django.contrib.auth.models import User
        from apps.marketplace.models import Item
        
        now = timezone.now()
        week_ago = now - timedelta(days=7)
        
        data = {
            'total_users': User.objects.count(),
            'new_users_this_week': User.objects.filter(date_joined__gte=week_ago).count(),
            'total_items': Item.objects.count(),
            'total_sales': Item.objects.aggregate(total=Sum('sales'))['total'] or 0,
            'total_views': Item.objects.aggregate(total=Sum('views'))['total'] or 0,
            'recent_items': list(
                Item.objects.order_by('-created_at')[:10].values('id', 'title', 'price', 'sales')
            ),
        }
        return Response(data)
