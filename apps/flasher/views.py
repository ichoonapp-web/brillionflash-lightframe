from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import LightPreset
from .serializers import LightPresetSerializer

class PresetListCreateView(generics.ListCreateAPIView):
    queryset = LightPreset.objects.all().order_by('-created_at')
    serializer_class = LightPresetSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class PresetRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LightPreset.objects.all()
    serializer_class = LightPresetSerializer
    permission_classes = [IsAuthenticated]

class TrendingPresetsView(generics.ListAPIView):
    serializer_class = LightPresetSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        return LightPreset.objects.filter(is_trending=True).order_by('-views')[:20]
