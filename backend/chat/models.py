from uuid import uuid4
from django.db import models


class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    chat_memory = models.TextField(null=False, blank=False)

    def __str__(self):
        return f"{self.id}"
