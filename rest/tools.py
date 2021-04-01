def delete_transaction(transaction):
    wallet = transaction.wallet
    wallet.balance -= transaction.amount
    wallet.save()


def execute_transaction(transaction_data):
    wallet = transaction_data['wallet']
    wallet.balance += transaction_data['amount']
    wallet.save()
