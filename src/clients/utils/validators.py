from django.core.exceptions import ValidationError


def validate_file_size(value):
    max_size_mb = 15
    max_size = max_size_mb * 1024 * 1024
    if value.size > max_size:
        raise ValidationError(
            f"The size of the file can't be more than {max_size_mb} MB, current size is "
            f"{round(value.size / (1024 * 1024), 2)} MB"
        )


def rating_validator(rating: int | float) -> None:
    if rating < 0 or rating > 10:
        raise ValidationError("The rating can't be less than 0 and more than 10")
