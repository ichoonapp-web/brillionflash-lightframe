import stripe
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
    
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        item_id = session['metadata'].get('item_id')
        buyer_id = session['metadata'].get('buyer_id')
        
        from .models import Item
        from django.contrib.auth.models import User
        
        item = Item.objects.get(id=item_id)
        buyer = User.objects.get(id=buyer_id)
        seller = item.creator
        admin = User.objects.get(id=os.getenv('ADMIN_UID', ''))
        
        # 70/30 Split
        seller.balance += item.price * Decimal('0.7')
        seller.save()
        admin.balance += item.price * Decimal('0.3')
        admin.save()
        
        item.sales += 1
        item.save()
    
    return JsonResponse({'status': 'ok'})
