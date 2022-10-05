from django.core.management.base import BaseCommand

import pandas

from reviews.models import (Category, Comment, Genre, GenreTitle,
                            Review, Title, User)


class Command(BaseCommand):
    help = "Loads data from children.csv"

    def handle(self, *args, **options):
        if User.objects.exists():
            User.objects.all().delete()

        users_data = pandas.read_csv('static/data/users.csv', sep=',')

        users = [
            User(
                id=row.get('id'),
                username=row.get('username'),
                email=row.get('email'),
                is_moderator=row.get('role') == 'moderator',
                is_staff=row.get('role') == 'admin',
                first_name=row.get('first_name'),
                last_name=row.get('last_name'),
                bio=row.get('bio'),
            ) for _, row in users_data.iterrows()
        ]

        User.objects.bulk_create(users)
        print('Успешная загрузка в БД User :)\n')

        if Genre.objects.exists():
            Genre.objects.all().delete()

        genre_data = pandas.read_csv('static/data/genre.csv', sep=',')

        genres = [
            Genre(
                id=row.get('id'),
                name=row.get('name'),
                slug=row.get('slug')
            ) for _, row in genre_data.iterrows()
        ]

        Genre.objects.bulk_create(genres)
        print('Успешная загрузка в БД Genre :)\n')

        if Category.objects.exists():
            Category.objects.all().delete()

        category_data = pandas.read_csv('static/data/category.csv', sep=',')

        categories = [
            Category(
                id=row.get('id'),
                name=row.get('name'),
                slug=row.get('slug')
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
                id=row.get('id'),
                name=row.get('name'),
                year=row.get('year'),
                category=Category.objects.get(id=row.get('category'))
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
                id=row.get('id'),
                title=Title.objects.get(id=row.get('title_id')),
                genre=Genre.objects.get(id=row.get('genre_id'))
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
                id=row.get('id'),
                title=Title.objects.get(pk=row.get('title_id')),
                text=row.get('text'),
                author=User.objects.get(id=row.get('author')),
                rating=row.get('score'),
                pub_date=row.get('pub_date'),
            ) for _, row in review_data.iterrows()
        ]

        Review.objects.bulk_create(reviews)
        print('Успешная загрузка в БД Review :)\n')

        #Модель Comments
        if Comment.objects.exists():
            Comment.objects.all().delete()

        comment_data = pandas.read_csv('static/data/comments.csv', sep=',')

        comments = [
            Comment(
                id=row.get('id'),
                review=Review.objects.get(id=row.get('review_id')),
                text=row.get('text'),
                author=User.objects.get(id=row.get('author')),
                pub_date=row.get('pub_date')
            ) for _, row in comment_data.iterrows()
        ]

        Comment.objects.bulk_create(comments)
        print('Успешная загрузка в БД Comment :)')
