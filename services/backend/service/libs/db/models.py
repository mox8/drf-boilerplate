import uuid
from django.utils import timezone
from django.db import models

from libs.utils import generate_random_string

# Short "null=True, blank=True" snippet
NB = {
    'null': True,
    'blank': True,
}


def generate_random_string_10() -> str:
    return generate_random_string(length=10)


class BaseModel(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def _pre_create(self):
        """Pre create hook. Do not call save() here."""
        pass

    def _pre_update(self):
        """Pre update hook. Do not call save() here."""
        pass

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        if self._state.adding:
            self._pre_create()
        else:
            self._pre_update()
        return super().save(*args, **kwargs)


class BaseInternalIdModel(BaseModel):
    internal_id = models.CharField(max_length=10, unique=True, default=generate_random_string_10)

    class Meta:
        abstract = True
