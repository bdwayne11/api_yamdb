from django.db.models import Avg
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import (Genre, Category, Title,
                                      Review, Comment)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category',)

    def get_rating(self, obj):
        reviews = Review.objects.filter(title_id=obj)
        result = reviews.all().aggregate(Avg('rating'))
        return float("{0:.2f}".format(result['rating__avg']))


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('title', 'author', 'pub_date', 'text', 'rating')
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title'),
                message='Вы уже оставляли свой отзыв к данному произведению!'
            )
        ]

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('review', 'author', 'pub_date', 'text')