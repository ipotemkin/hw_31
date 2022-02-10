SKYVITO PROJECT
================

Homework 27
-----------

URLS realized:
> **Testing screen**
>> `GET /ads` 
> ```json
> {"status": "ok"}
> ``` 

> **Cписок всех объявлений**
>> `GET /ads/ad`
> ```json
>  [
>    {
>        "pk": 1,
>        "name": "Сибирская котята, 3 месяца",
>        "author": "Павел",
>        "price": 2500,
>        "description": "Продаю сибирских котят, возвраст 3 месяца.\nОчень милые и ручные.\nЛоточек знают на пятерку, кушают премиум корм.\nЖдут любящих и заботливых хояев. Больше фотографий отправлю в личку, цена указана за 1 котенка.",
>        "address": "Москва, м. Студенческая",
>        "is_published": true
>    },
>    {
>        "pk": 2,
>        "name": "Стратегия голубого океана\n",
>        "author": "Павел",
>        "price": 650,
>        "description": "Твердый переплет, состояние прекрасное. По всем вопросам лучше писать, звонок могу не услышать. Передам у м. Студенческая.",
>        "address": "Москва, м. Студенческая",
>        "is_published": true
>    }
>  ]
>```

> **Объявление с указанным ID**
>> `GET /ads/ad/id`
> ```json
>    {
>        "pk": 1,
>        "name": "Сибирская котята, 3 месяца",
>        "author": "Павел",
>        "price": 2500,
>        "description": "Продаю сибирских котят, возвраст 3 месяца.\nОчень милые и ручные.\nЛоточек знают на пятерку, кушают премиум корм.\nЖдут любящих и заботливых хояев. Больше фотографий отправлю в личку, цена указана за 1 котенка.",
>        "address": "Москва, м. Студенческая",
>        "is_published": true
>    }
> ```

> **Добавить объявление**
>> `POST /ads/ad/`
> ```json
>    {
>        "name": "Сибирская котята, 3 месяца",
>        "author": "Павел",
>        "price": 2500,
>        "description": "Продаю сибирских котят, возвраст 3 месяца.\nОчень милые и ручные.\nЛоточек знают на пятерку, кушают премиум корм.\nЖдут любящих и заботливых хояев. Больше фотографий отправлю в личку, цена указана за 1 котенка.",
>        "address": "Москва, м. Студенческая",
>        "is_published": true
>    }
> ```


> **Cписок всех категорий**
>> `GET /ads/cat`
> ```json
> [
>    {
>        "pk": 1,
>        "name": "Котики"
>    },
>    {
>        "pk": 2,
>        "name": "Песики"
>    }
> ]
> ```

> **Категория с указанным ID**
>> `GET /ads/cat/id`
> ```json
>    {
>        "pk": 1,
>        "name": "Котики"
>    }
> ```

> **Добавить категорию**
>> `POST /ads/cat/`
> ```json
>    {
>        "name": "Котики"
>    }
> ```


Dependencies
------------

1. Django
2. Pydantic
