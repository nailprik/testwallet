from rest_framework import viewsets, mixins

from rest.models import Wallet, Transaction
from rest.serializers import WalletSerializer, TransactionSerializer
from rest.tools import delete_transaction


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


class TransactionViewSet(viewsets.GenericViewSet,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filterset_fields = ['wallet__name']

    def perform_destroy(self, instance):
        delete_transaction(instance)
        instance.delete()
