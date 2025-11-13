from django.http import Http404
from rest_framework.views import APIView
from .models import Profile, CustomUser
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import CustomUserSerializer, ProfileSerializer
from datastore.permissions import IsOwnerOrReadOnly


# Profile views
class ProfileList(APIView):
    def get(self, request):
        users = CustomUser.objects.select_related('profile').all() 
        serializer = CustomUserSerializer(users, many=True, context={'request': request})
        return Response(serializer.data)

# Profile detail view
class UserProfileDetail(APIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsOwnerOrReadOnly]
    def get_object(self, pk):
        return get_object_or_404(CustomUser.objects.select_related('profile'), pk=pk)

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        """
        Delete a user and their related profile.
        """
        user = self.get_object(pk)
        user.delete()
        return Response({"detail": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)