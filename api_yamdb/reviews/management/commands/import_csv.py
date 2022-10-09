from django.core.management.base import BaseCommand

import pandas

from reviews.models import (Category, Comment, Genre, GenreTitle,
                            Review, Title, User)


class Command(BaseCommand):
    help = "Loads data from csv"

    def handle(self, *args, **options):
        if User.objects.exists():
            User.objects.all().delete()

        users_data = pandas.read_csv('static/data/users.csv', sep=',')

        users = [
            User(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                is_moderator=row['role'] == 'moderator',
                is_staff=row['role'] == 'admin',
                first_name=row['first_name'],
                last_name=row['last_name'],
                bio=row['bio']
            ) for _, row in users_data.iterrows()
        ]

        User.objects.bulk_create(users)
        print('Успешная загрузка в БД User :)\n')

        if Genre.objects.exists():
            Genre.objects.all().delete()

        genre_data = pandas.read_csv('static/data/genre.csv', sep=',')

        genres = [
            Genre(
                id=row['id'],
                name=row['name'],
                slug=row['slug'],
            ) for _, row in genre_data.iterrows()
        ]

        Genre.objects.bulk_create(genres)
        print('Успешная загрузка в БД Genre :)\n')

        if Category.objects.exists():
            Category.objects.all().delete()

        category_data = pandas.read_csv('static/data/category.csv', sep=',')

        categories = [
            Category(
                id=row['id'],
                name=row['name'],
                slug=row['slug']
            ) for _, row in category_data.iterrows()
        ]

        Category.objects.bulk_create(categories)
        print('Успешная загрузка в БД Category :)\n')

        # Модель Title
        if Title.objects.exists():
            Title.objects.all().delete()

        title_data = pandas.read_csv('static/data/titles.csv', sep=',')

        titles = [
            Title(
                id=row['id'],
                name=row['name'],
                year=row['year'],
                category=Category.objects.get(id=row['category'])
            ) for _, row in title_data.iterrows()
        ]

        Title.objects.bulk_create(titles)
        print('Успешная загрузка в БД Title :)\n')

        # Модель GenreTitle
        if GenreTitle.objects.exists():
            GenreTitle.objects.all().delete()

        genretitle_data = pandas.read_csv(
            'static/data/genre_title.csv', sep=',')

        genretitles = [
            GenreTitle(
                id=row['id'],
                title=Title.objects.get(id=row['title_id']),
                genre=Genre.objects.get(id=row['genre_id'])
            ) for _, row in genretitle_data.iterrows()
        ]

        GenreTitle.objects.bulk_create(genretitles)
        print('Успешная загрузка в БД GenreTitle :)\n')

        # Модель Review
        if Review.objects.exists():
            Review.objects.all().delete()

        review_data = pandas.read_csv('static/data/review.csv', sep=',')

        reviews = [
            Review(
                id=row['id'],
                title=Title.objects.get(pk=row['title_id']),
                text=row['text'],
                author=User.objects.get(id=row['author']),
                rating=row['score'],
                pub_date=row['pub_date'],
            ) for _, row in review_data.iterrows()
        ]

        Review.objects.bulk_create(reviews)
        print('Успешная загрузка в БД Review :)\n')

        # Модель Comments
        if Comment.objects.exists():
            Comment.objects.all().delete()

        comment_data = pandas.read_csv('static/data/comments.csv', sep=',')

        comments = [
            Comment(
                id=row['id'],
                review=Review.objects.get(id=row['review_id']),
                text=row['text'],
                author=User.objects.get(id=row['author']),
                pub_date=row['pub_date']
            ) for _, row in comment_data.iterrows()
        ]

        Comment.objects.bulk_create(comments)
        print('Успешная загрузка в БД Comment :)')
