from datetime import datetime

from django.core.exceptions import ValidationError


def validate_year(value):
    date = datetime.now()
    if value > date.year and value <= 1800:
        raise ValidationError('Текущий год не может быть меньше'
                              'введенного и меньше 1800г.')
