# REST API Кошелек
Авторизация
```
/api-token-auth
request body:
    username
    password
```
Доступные методы:

```
/api
    /wallets
        get:
            description: Выдать список кошельков
        post:
            description: Добавить кошелек
        /{walletId}
                get:
                    description: Получить кошелек по id
            update:
                description: Изменить кошелек
    /transactions
            get:
                description: Выдать список всех транзакций
            post:
                description: Добавить транзакцию
            ?wallet__name={walletName}
                get:
                    description: Получить список транзакций по данному кошельку
            /{transactiontId}
                    get:
                        description: Получить транзакцию по id
```