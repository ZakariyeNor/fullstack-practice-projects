from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from rest_framework import status

from rest_framework.decorators import api_view, throttle_classes
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters

from django.views.decorators.cache import cache_page
from django.utils.cache import patch_cache_control

from .models import MenuItem
from .serializers import MenuItemSerializer
from .caching_utils import get_or_set_cache, CACHE_TTL

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes

from django.contrib.auth.models import Group, User

from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from .throttles import TenCallsPerMinute

import bleach

# Cache the entire view at the web server level (DRF / Django)
@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
    throttle_classes = [AnonRateThrottle, TenCallsPerMinute]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__title', 'price']
    search_fields = ['title', 'price', 'category__title']
    ordering_fields = ['price', 'title', 'stock']
    
    def get_queryset(self):
        # Database-level caching with Redis
        return get_or_set_cache("menu_items_all", lambda: MenuItem.objects.all())

    def finalize_response(self, request, response, *args, **kwargs):
        # Client-side caching header
        patch_cache_control(response, public=True, max_age=CACHE_TTL)
        return super().finalize_response(request, response, *args, **kwargs)

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class SingelMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    
    throttle_classes = [AnonRateThrottle, TenCallsPerMinute]
    
    def get_queryset(self):
        # Cache individual item queries
        return get_or_set_cache("menu_items_all", lambda: MenuItem.objects.all())

    def finalize_response(self, request, response, *args, **kwargs):
        patch_cache_control(response, public=True, max_age=CACHE_TTL)
        return super().finalize_response(request, response, *args, **kwargs)


@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"message": "Classified"})


@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name='Manager').exists():
        return Response({"message": "Manager duty"})
    else:
        return Response({"message": "You are not allowed"}, 403)

# High level user role management
@api_view(['POST'])
@permission_classes([IsAdminUser])
def manager(request):
    username = request.data['username']
    if username:
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name='Manager')
        
        if request.method == 'POST':
            managers.user_set.add(user)
        elif request.method == 'DELETE':
            managers.user_set.remove(user)
        return Response({"message": "Managers responsibility"})
    
    return Response({"message": "Allowed only for anagers"},  status.HTTP_400_BAD_REQUEST)


# Api call limit
@api_view(['GET'])
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({"message": "Successful"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@throttle_classes([TenCallsPerMinute])
def throttle_user(request):
    return Response({"message": "Successful"})
