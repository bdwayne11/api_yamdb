from django.urls import path, include
from rest_framework import routers

from .views import (GenreViewSet, CategoryViewSet,
                    TitleViewSet, ReviewViewSet,
                    CommentViewSet)

app_name = 'api'

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
                CommentViewSet)
#Здесь router.register('users', UserViewSet) ???

urlpatterns = [
    path('v1/', include(router.urls)),
]
