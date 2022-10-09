from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, IsAuthenticated

from .filters import TitleFilter
from .permissions import (OnlySafeMethodsOrStaff, IsAdminOrUserReadOnly,
                          AdminModerAuthor)
from .serializers import (GenreSerializer, CategorySerializer,
                          TitleGetSerializer, ReviewSerializer,
                          CommentSerializer, TitlePostSerializer)
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
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (OnlySafeMethodsOrStaff,)
    lookup_field = 'slug'


class CategoryViewSet(GetListDestroyCreate):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (OnlySafeMethodsOrStaff,)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrUserReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ["get", "post", "head", "patch", "delete"]

    def get_serializer_class(self):
        if self.request.method not in ('POST', 'PATCH'):
            return TitleGetSerializer
        return TitlePostSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AdminModerAuthor,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)

    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         self.permission_classes == (AllowAny,)
    #     elif self.request.method == 'POST':
    #         self.permission_classes == (IsAuthenticated,)
    #     else:
    #         self.permission_classes == (AdminModerAuthor,)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AdminModerAuthor,)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)

    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         self.permission_classes == (AllowAny,)
    #     elif self.request.method == 'POST':
    #         self.permission_classes == (IsAuthenticated,)
    #     else:
    #         self.permission_classes == (AdminModerAuthor,)