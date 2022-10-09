from django.db.models import Avg
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


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


class TitlePostSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class TitleGetSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField("get_rating")
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category',)

    def get_rating(self, title):
        reviews = Review.objects.filter(title=title)
        rating = reviews.all().aggregate(Avg("score"))
        result = rating["score__avg"]
        return result


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    title = serializers.SlugRelatedField(
        slug_field='id',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    def validate(self, data):
        title = self.context["view"].kwargs["title_id"]
        author = self.context["request"].user
        is_exists = Review.objects.filter(title=title, author=author)
        if self.context["request"].method != "PATCH":
            if is_exists:
                raise ValidationError(
                    "Вы уже оставляли ревью к этому произведению")
        return data

    class Meta:
        model = Review
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date',)
