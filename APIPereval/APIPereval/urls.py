from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from pereval_app.views import PerevalViewSet
from .yasg import urlpatterns as doc_urls


router = DefaultRouter()
router.register(r'pereval', PerevalViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]

urlpatterns += doc_urls
