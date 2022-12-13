from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, get_available_image_extensions

from libs.django.validators import validate_svg


class SVGAndImageFieldForm(forms.ImageField):
    """Expands ImageField to .svg files"""

    default_validators = [
        FileExtensionValidator(
            allowed_extensions=get_available_image_extensions() + ['svg'],
        ),
    ]

    def to_python(self, data):
        try:
            f = super().to_python(data)
        except ValidationError:
            return validate_svg(data)

        return f
