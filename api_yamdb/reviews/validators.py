from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_year(value):
    if value > timezone.now():
        raise ValidationError('Текущий год не может быть больше введенного')
