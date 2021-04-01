from rest_framework import serializers

from rest.models import Wallet, Transaction
from rest.tools import execute_transaction


class WalletSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wallet
        fields = ['name', 'balance']
        read_only_fields = ['balance']


class TransactionSerializer(serializers.ModelSerializer):
    wallet = serializers.SlugRelatedField(queryset=Wallet.objects.all(), slug_field='name')

    class Meta:
        model = Transaction
        fields = '__all__'

    def create(self, validated_data):
        execute_transaction(validated_data)
        instance = super(TransactionSerializer, self).create(validated_data)
        return instance

