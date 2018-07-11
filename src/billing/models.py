from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = get_user_model()
# Create your models here.

CASH_IN = 'cash_in'
CASH_OUT = 'cash_out'

TRANSACTION_ACTIONS = (
    (CASH_IN, "Пополнение"),
    (CASH_OUT, "Списание"),
)


class CrystalTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u'Сумма')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    object_id = models.PositiveIntegerField(null=True)
    action = models.CharField(choices=TRANSACTION_ACTIONS, max_length=50, verbose_name=u'Действия')
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = u'Транзакция кристала'
        verbose_name_plural = u'Транзакции кристалов'
