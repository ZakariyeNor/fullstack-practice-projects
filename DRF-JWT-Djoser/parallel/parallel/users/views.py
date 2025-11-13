from rest_framework import viewsets, permissions, generics  , status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import CustomUser
from .serializers import CustomUserSerializer, RegisterSerializer

# JWT
from rest_framework_simplejwt.tokens import RefreshToken


# new user
User = get_user_model()


# Main view
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = CustomUserSerializer

# Register new user
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate JWT token pair
        refresh = RefreshToken.for_user(user)
        data = {
            "user": CustomUserSerializer(user, context=self.get_serializer_context()).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }
        return Response(data, status=status.HTTP_201_CREATED)

# Current user
class CurrentUserView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
    def get_object(self):
        return self.request.user
    