from django.db import models
import uuid


class BaseModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    created_on = models.DateField(auto_now_add=True, editable=False)
    updated_on = models.DateField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ("-created_on",)
