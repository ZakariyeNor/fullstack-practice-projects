from rest_framework import generics, permissions
from .models import CustomUser
from .serializers import CustomUserSerializer, ProfileSerializer

# -------------------------
# List all users with nested profiles
# -------------------------
class ProfileListView(generics.ListAPIView):
    queryset = CustomUser.objects.prefetch_related('profile').all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]  # or IsAdminUser if needed


# -------------------------
# Retrieve detail of a user with nested profile
# -------------------------
class ProfileDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.prefetch_related('profile').all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return super().get_object()