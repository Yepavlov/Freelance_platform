from datetime import date

from django.core.exceptions import ValidationError


def validate_file_size(value):
    max_size_mb = 15
    max_size = max_size_mb * 1024 * 1024
    if value.size > max_size:
        raise ValidationError(
            f"The size of the file can't be more than {max_size_mb} MB, current size is "
            f"{round(value.size / (1024 * 1024), 2)} MB"
        )


def birth_date_validator(birth_date: date) -> None:
    if birth_date:
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if age < 14:
            raise ValidationError("Person must be at least 14 years old.")


def extension_validator(file_name: str) -> None:
    if file_name:
        file_extension = file_name.name.split(".")[-1].lower()
        allowed_extensions = ["pdf", "doc", "docx"]
        if file_extension not in allowed_extensions:
            raise ValidationError("Only PDF, DOC, and DOCX files are allowed.")


def rating_validator(rating: int | float) -> None:
    if rating < 0 or rating > 10:
        raise ValidationError("The rating can't be less than 0 and more than 10")
