import datetime

from django.core.exceptions import ValidationError


def schedule_time_validator(value):
    if value < datetime.datetime.now():
        raise ValidationError(
            'Проверьте правильность введенной даты'
        )
