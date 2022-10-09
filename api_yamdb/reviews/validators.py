from datetime import datetime
from django.core.exceptions import ValidationError


def validate_year(value):
    date = datetime.now()
    if value > date.year:
        raise ValidationError('Текущий год не может быть больше введенного')
