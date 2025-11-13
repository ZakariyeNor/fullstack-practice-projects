from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# Register our custom viewset
router.register('users', views.CustomUserViewSet) 
# Note: The base path for this will be 'api/users/' based on your project urls

urlpatterns = [
    # Main view
    path('main/', views.first_page, name='first-main'),

    # Include the router URLs
    path('', include(router.urls)),
    
    # Profiles list 
    path('profiles/', views.UserProfileList.as_view(), name='profile-list'),

    # Profiles detail 
    path('profiles/<int:pk>/', views.UserProfileDetail.as_view(), name='profile-detail'),
]