from django.urls import path
from profiles import views

urlpatterns = [
    path('profiles/', views.ProfileList.as_view(), name='profiles'),
    path('profiles-detail/<int:pk>/', views.ProfileDetail.as_view(), name='profiles-detail'),
]