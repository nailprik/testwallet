import datetime
import json

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from rest.models import Wallet, Transaction
from rest.serializers import WalletSerializer, TransactionSerializer


class WalletApiTestCase(APITestCase):
    def setUp(self):
        self.wallet = Wallet.objects.create(name='test')
        self.user = User.objects.create(username='testuser')

    def test_get(self):
        url = reverse('wallet-detail', args=(self.wallet.id,))
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        wallet_serialized_data = WalletSerializer(self.wallet).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data, wallet_serialized_data)

    def test_create(self):
        url = reverse('wallet-list')
        data ={
            'name': 'test_wallet'
        }
        json_data = json.dumps(data)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_update(self):
        url = reverse('wallet-detail', args=(self.wallet.id,))
        data = {
            'name': 'test_wallet'
        }
        json_data = json.dumps(data)
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.wallet.refresh_from_db()
        self.assertEqual('test_wallet', self.wallet.name)


class TransactionTestCase(APITestCase):
    def setUp(self):
        self.wallet1 = Wallet.objects.create(name='test1')
        self.wallet2 = Wallet.objects.create(name='test2')
        self.user = User.objects.create(username='testuser')
        self.transaction1 = Transaction.objects.create(wallet=self.wallet1, amount='1000.00',
                                                      date=datetime.datetime.now(tz=timezone.utc), info='Test transaction')
        self.transaction2 = Transaction.objects.create(wallet=self.wallet2, amount='1000.00',
                                                      date=datetime.datetime.now(tz=timezone.utc),
                                                      info='Test transaction')

    def test_wallet_transactions(self):
        url = reverse('transaction-list')
        print(url)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url+f'?wallet__name={self.wallet1.name}')
        transactions_serialized_data = TransactionSerializer(Transaction.objects.filter(wallet=self.wallet1), many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data, transactions_serialized_data)

    def test_get(self):
        url = reverse('transaction-detail', args=(self.transaction1.id,))
        print(url)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        transactions_serialized_data = TransactionSerializer(Transaction.objects.get(id=self.transaction1.id)).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data, transactions_serialized_data)

    def test_create(self):
        url = reverse('transaction-list')
        balance_before = self.wallet1.balance
        data = {
            'wallet': self.wallet1.name,
            'amount': '10000.00',
            'info': 'Test transaction',
            'date': str(datetime.datetime.now(tz=timezone.utc))
        }
        json_data = json.dumps(data)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.wallet1.refresh_from_db()
        balance_after = self.wallet1.balance
        self.assertEqual(balance_after, balance_before + 10000)