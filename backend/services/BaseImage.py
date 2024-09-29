from django.db import models

from versatileimagefield.fields import VersatileImageField


class BaseImage(models.Model):
    """Basic model for images"""
    title = models.CharField(max_length=200, null=True, blank=True)
    alt = models.CharField(max_length=200, null=True, blank=True)
    image = VersatileImageField(null=True, blank=True, upload_to='images')

    class Meta:
        """Abstract-чтобы не создавать миграций"""
        abstract = True
        verbose_name = "Image"
        verbose_name_plural = "Images"

    def __str__(self):
        res = self.image.url
        if self.title:
            res = self.title

        return res
