from django.core.exceptions import ValidationError

from libs.utils import is_svg


def validate_svg(file):
    if not is_svg(file):
        raise ValidationError("Uploaded file is not an image or SVG file")
    return file
