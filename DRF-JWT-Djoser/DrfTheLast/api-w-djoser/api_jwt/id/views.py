from rest_framework import generics
from djoser.views import UserViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.decorators import api_view

from .models import UserProfile

from .serializers import UserProfileSerializer, UserProfileUpdateSerializer

def get_tokens_for_user(user):
    """Helper function to generate tokens."""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class CustomUserViewSet(UserViewSet):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        # Generate tokens manually for the newly created user
        tokens = get_tokens_for_user(user)
        
        # Combine user data and tokens in the response data
        user_data = serializer.data
        user_data.update(tokens)
        
        return Response(user_data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        # We need this method to save the user instance correctly in the view context
        return serializer.save()


class UserProfileList(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileUpdateSerializer


@api_view(['GET'])
def first_page(request):
    return Response({'Print': 'Main data'})