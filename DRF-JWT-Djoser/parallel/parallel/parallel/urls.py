from django.contrib import admin
from django.urls import path, include

# For static images
from django.conf import settings
from django.conf.urls.static import static

# JWT
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView,
)


# URLs
urlpatterns = [
    path('admin/', admin.site.urls),
    
    # JWT endpoints 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Users app
    path('api/users/', include('users.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
