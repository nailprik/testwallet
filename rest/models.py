from django.db import models


class Wallet(models.Model):
    name = models.CharField(max_length=20, verbose_name='Название кошелька', unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Баланс кошелька', default=0)


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='wallet', verbose_name='Кошелек')
    date = models.DateTimeField(verbose_name='Время транзакции')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма транзакции')
    info = models.TextField(verbose_name='О транзакции')


