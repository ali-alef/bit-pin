from django.urls import path, include
from rest_framework.routers import DefaultRouter
from content.views import ContentViewSet, ReviewViewSet

router = DefaultRouter()
router.register('contents', ContentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('reviews/', ReviewViewSet.as_view({'post': 'post'}), name='create_review'),
]
