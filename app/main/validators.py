from rest_framework.exceptions import ValidationError


def validate_feedback_mark(value):
    if value not in [x / 2 for x in range(0, 11)]:
        raise ValidationError({'mark': 'Incorrect mark value'})


def validate_contains_numbers(value):
    if any(map(str.isdigit, value)):
        raise ValidationError('The value contains numbers')
