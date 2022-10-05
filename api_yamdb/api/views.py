from rest_framework import viewsets, mixins
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import get_object_or_404

from .permissions import OnlySafeMethodsOrStaff
from .serializers import (GenreSerializer, CategorySerializer,
                          TitleSerializer, ReviewSerializer,
                          CommentSerializer)
from reviews.models import (Genre, Category, Title,
                                      Review, Comment)


class GetListDestroyCreate(mixins.ListModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.CreateModelMixin,
                           viewsets.GenericViewSet):
    pass


class GenreViewSet(GetListDestroyCreate):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = (OnlySafeMethodsOrStaff,)


class CategoryViewSet(GetListDestroyCreate):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = (OnlySafeMethodsOrStaff,)


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    queryset = Title.objects.all()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Comment.objects.all()
