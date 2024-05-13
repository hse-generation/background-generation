from django.db import models
from account.models import Users


class Sources(models.Model):
    name = models.CharField("Название источника", max_length=10000, null=True)
    status = models.IntegerField("Статус активности", null=False, default=1)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Источник'
        verbose_name_plural = 'Источники'
        db_table = 'sources'
