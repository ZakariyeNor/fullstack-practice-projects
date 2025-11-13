from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path('menu-items/', views.MenuItemView.as_view(), name='menu'),
    path('menu-items/<int:pk>/', views.SingelMenuItemView.as_view(), name='single-item'),
    path('secret/', views.secret, name='secret'),
    path('manager/', views.manager_view, name='manager'),
    path('groups/manager/users/', views.manager, name='manager'),
    path('api-auth-token/', obtain_auth_token),
    path('throttle/', views.throttle_check, name='throttle'),
    path('throttle_user/', views.throttle_user, name='throttle-user')
]