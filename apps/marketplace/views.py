import stripe
import os
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Item
from .serializers import ItemSerializer

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

class ItemListCreateView(generics.ListCreateAPIView):
    queryset = Item.objects.all().order_by('-created_at')
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class ItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data.get('itemId')
        item = Item.objects.get(id=item_id)
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': item.title},
                    'unit_amount': int(item.price * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://web-production-1bf52.up.railway.app/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='https://web-production-1bf52.up.railway.app/cancel',
            metadata={'item_id': str(item.id), 'buyer_id': str(request.user.id) if request.user.is_authenticated else ''}
        )
        return JsonResponse({'url': session.url})
