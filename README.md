SKYVITO PROJECT
================

Homework 28
-----------

URLS realized:
> **Testing screen**
>> `GET /` 
> ```json
> {"status": "ok"}
> ``` 

> **Cписок всех объявлений**
>> `GET /ads/ad/` или `GET /ads/ads/`
> ```json
>  [
>    {
>       "pk": 1,
>       "name": "Сибирская котята, 3 месяца",
>       "author_id": 1,
>       "author": "Павел",
>       "price": 2500,
>       "description": "Продаю сибирских котят, возраст 3 месяца.\nОчень милые и ручные.\nЛоточек знают на пятерку, кушают премиум корм.\nЖдут любящих и заботливых хояев. Больше фотографий отправлю в личку, цена указана за 1 котенка.",
>       "is_published": true,
>       "category_id": 1,
>       "category": "Котики",
>       "image": "/media/img/pic1.jpg"
>    },
>    {
>       "pk": 2,
>       "name": "Стратегия голубого океана\n",
>       "author_id": 5,
>       "author": "Ирина",
>       "price": 650,
>       "description": "Твердый переплет, состояние прекрасное. По всем вопросам лучше писать, звонок могу не услышать. Передам у м. Студенческая.",
>       "is_published": true,
>       "category_id": 3,
>       "category": "Книги",
>       "image": "No picture yet"
>    }
>  ]
>```

> **Cписок всех объявлений с пагинацией**
>> `GET /ads/ad/?page=2` или `GET /ads/ads/?page=2`
> ```json
>  {
>    "items": [{
>       "pk": 1,
>       "name": "Сибирская котята, 3 месяца",
>       "author_id": 1,
>       "author": "Павел",
>       "price": 2500,
>       "description": "Продаю сибирских котят, возраст 3 месяца.\nОчень милые и ручные.\nЛоточек знают на пятерку, кушают премиум корм.\nЖдут любящих и заботливых хояев. Больше фотографий отправлю в личку, цена указана за 1 котенка.",
>       "is_published": true,
>       "category_id": 1,
>       "category": "Котики",
>       "image": "/media/img/pic1.jpg"
>    },
>    {
>       "pk": 2,
>       "name": "Стратегия голубого океана\n",
>       "author_id": 5,
>       "author": "Ирина",
>       "price": 650,
>       "description": "Твердый переплет, состояние прекрасное. По всем вопросам лучше писать, звонок могу не услышать. Передам у м. Студенческая.",
>       "is_published": true,
>       "category_id": 3,
>       "category": "Книги",
>       "image": "No picture yet"
>    }],
>   "total": 23,
>   "per_page": 2,
>   "num_pages": 12
>  }
>```

> **Cписок всех объявлений в html**
>> `GET /ads/ad/html`

> **Объявление с указанным ID**
>> `GET /ads/ad/id`
> ```json
>    {
>       "pk": 1,
>       "name": "Сибирская котята, 3 месяца",
>       "author_id": 1,
>       "author": "Павел",
>       "price": 2500,
>       "description": "Продаю сибирских котят, возвраст 3 месяца.\nОчень милые и ручные.\nЛоточек знают на пятерку, кушают премиум корм.\nЖдут любящих и заботливых хояев. Больше фотографий отправлю в личку, цена указана за 1 котенка.",
>       "is_published": true,
>       "category_id": 1,
>       "category": "Котики",
>       "image": "/media/img/pic1.jpg"
>    }
> ```

> **Объявление с указанным ID в html**
>> `GET /ads/ad/html/id`


> **Добавить объявление**
>> `POST /ads/ad/`
> ```json
>    {
>       "name": "Сибирская котята, 3 месяца",
>       "author_id": 1,
>       "author": "Павел",
>       "price": 2500,
>       "description": "Продаю сибирских котят, возвраст 3 месяца.\nОчень милые и ручные.\nЛоточек знают на пятерку, кушают премиум корм.\nЖдут любящих и заботливых хояев. Больше фотографий отправлю в личку, цена указана за 1 котенка.",
>       "is_published": true,
>       "category_id": 1,
>       "category": "Котики",
>       "image": "No picture yet"
>    }
> ```


> **Изменить объявление**
>> `PATCH /ads/ad/id/update`
> ```json
>    {
>       "name": "Сибирская котята, 3 месяца",
>       "author_id": 1,
>       "author": "Павел",
>       "price": 2500,
>       "description": "Продаю сибирских котят, возвраст 3 месяца.\nОчень милые и ручные.\nЛоточек знают на пятерку, кушают премиум корм.\nЖдут любящих и заботливых хояев. Больше фотографий отправлю в личку, цена указана за 1 котенка.",
>       "is_published": true,
>       "category_id": 1,
>       "category": "Котики",
>       "image": "No picture yet"
>    }
> ```

> **Добавить/обновить картинку в объявление**
>> `POST /ads/ad/id/upload_image`  
> `ContentType 'multipart/form-data'`  
> `FILES: "image"`
> ```json
>    {
>       "name": "Сибирская котята, 3 месяца",
>       "author_id": 1,
>       "author": "Павел",
>       "price": 2500,
>       "description": "Продаю сибирских котят, возвраст 3 месяца.\nОчень милые и ручные.\nЛоточек знают на пятерку, кушают премиум корм.\nЖдут любящих и заботливых хояев. Больше фотографий отправлю в личку, цена указана за 1 котенка.",
>       "is_published": true,
>       "category_id": 1,
>       "category": "Котики",
>       "image": "/media/img/new.jpg"
>    }
> ```

> **Удалить объявление**
>> `DELETE /ads/ad/id/delete/`

> **Cписок всех категорий**
>> `GET /ads/cat/`
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
>> `GET /ads/cat/id/`
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


> **Изменить категорию**
>> `PATCH /ads/cat/id/update`
> ```json
>    {
>        "name": "Котики"
>    }
> ```

> **Удалить категорию**
>> `DELETE /ads/cat/id/delete`


> **Cписок всех пользователей (возможна пагинация)**
>> `GET /ads/user/`
> ```json
> [
>   {
>       "id": 5,
>       "username": "Ирина",
>       "first_name": null,
>       "last_name": null,
>       "role": null,
>       "age": 17,
>       "locations": [
>           "Москва",
>           "Свиблово"
>       ],
>       "total_ads": 1
>   },
>  {
>       "id": 4,
>       "username": "Светлана",
>       "first_name": null,
>       "last_name": null,
>       "role": null,
>       "age": 19,
>       "locations": [],
>       "total_ads": 0
>  }
> ]
> ```

> **Пользователь с указанным ID**
>> `GET /ads/user/id/`
> ```json
> {
>    "id": 5,
>    "username": "Ирина",
>    "first_name": null,
>    "last_name": null,
>    "role": null,
>    "age": 17,
>    "locations": [
>       "Москва",
>       "Свиблово"
>     ]
> }
> ```

> **Добавить пользователя**
>> `POST /ads/user/create`

> **Изменить пользователя**
>> `PATCH /ads/user/id/update`

> **Удалить пользователя**
>> `DELETE /ads/user/id/delete`

Database connection and data loading
------------
- docker-run.sh – старт контейнера с СУБД PostgreSQL
- migrate-loadall.sh – миграция структур и загрузка данных

Dependencies
------------

1. Django
2. Pydantic
3. psycopg2
