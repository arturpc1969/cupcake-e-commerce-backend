from django.db import models

class BaseModel(models.Model):
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def soft_delete(self):
        """Mark as inactive instead of removing"""
        self.active = False
        self.save()

    def restore(self):
        """Restores an inactivated record"""
        self.active = True
        self.save()


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)


