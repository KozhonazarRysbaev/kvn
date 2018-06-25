from django.db import models
from django.utils.translation import ugettext_lazy as _


class City(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name = _('Город')
        verbose_name_plural = _('Города')
        ordering = ['name']

    def __str__(self):
        return self.name
