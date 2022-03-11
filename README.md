SKYVITO PROJECT
================

Homework 30
-----------

URLS realized:
> **Testing screen**
>> `GET /` 
> ```json
> {"status": "ok"}
> ``` 

> **Cписок всех объявлений**
>> `GET /ads/`  
> 
> **Возможна пагинация и фильтрация:**  
> - по имени объявления: GET ads/?text=кот  
> - по ID категории: GET ads/?cat=1
> - по названию локации: GET ads/?location=Москва
> - по минимальной цене: GET ads/?price_from=1000
> - по максимальной цене: GET ads/?price_to=5000
> - по имени автора: GET /ads/?username=Mike
> - по любому набору, указанных критериев
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
>> `GET /ads/?page=2`
> ```json
>  {
>    "items": [{
>       "pk": 1,
>       "name": "Сибирская котята, 3 месяца",
>       "author": 1,
>       "price": 2500,
>       "description": "Продаю сибирских котят, возраст 3 месяца.\nОчень милые и ручные.\nЛоточек знают на пятерку, кушают премиум корм.\nЖдут любящих и заботливых хояев. Больше фотографий отправлю в личку, цена указана за 1 котенка.",
>       "is_published": true,
>       "category": 1,
>       "image": "/media/img/pic1.jpg"
>    },
>    {
>       "pk": 2,
>       "name": "Стратегия голубого океана\n",
>       "author": 5,
>       "price": 650,
>       "description": "Твердый переплет, состояние прекрасное. По всем вопросам лучше писать, звонок могу не услышать. Передам у м. Студенческая.",
>       "is_published": true,
>       "category": 3,
>       "image": null
>    }],
>   "total": 23,
>   "per_page": 2,
>   "num_pages": 12
>  }
>```

> **Cписок всех объявлений в html**
>> `GET /ads/html`

> **Объявление с указанным ID**
>> `GET /ads/id/`
> ```json
>    {
>       "pk": 1,
>       "name": "Сибирская котята, 3 месяца",
>       "author": 1,
>       "price": 2500,
>       "description": "Продаю сибирских котят, возвраст 3 месяца.\nОчень милые и ручные.\nЛоточек знают на пятерку, кушают премиум корм.\nЖдут любящих и заботливых хояев. Больше фотографий отправлю в личку, цена указана за 1 котенка.",
>       "is_published": true,
>       "category": 1,
>       "image": "/media/img/pic1.jpg"
>    }
> ```

> **Объявление с указанным ID в html**
>> `GET /ads/html/id/`


> **Добавить объявление**
>> `POST /ads/`
> ```json
>    {
>       "name": "Сибирская котята, 3 месяца",
>       "author": 1,
>       "price": 2500,
>       "description": "Продаю сибирских котят, возвраст 3 месяца.\nОчень милые и ручные.\nЛоточек знают на пятерку, кушают премиум корм.\nЖдут любящих и заботливых хояев. Больше фотографий отправлю в личку, цена указана за 1 котенка.",
>       "is_published": true,
>       "category": 1,
>       "image": null
>    }
> ```


> **Изменить объявление**
>> `PATCH /ads/id/`
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
>> `POST /ads/id/upload_image/`  
> `ContentType 'multipart/form-data'`  
> `FILES: "image"`
> ```json
>    {
>       "name": "Сибирская котята, 3 месяца",
>       "author": 1,
>       "price": 2500,
>       "description": "Продаю сибирских котят, возвраст 3 месяца.\nОчень милые и ручные.\nЛоточек знают на пятерку, кушают премиум корм.\nЖдут любящих и заботливых хояев. Больше фотографий отправлю в личку, цена указана за 1 котенка.",
>       "is_published": true,
>       "category": 1,
>       "image": "/media/img/new.jpg"
>    }
> ```

> **Удалить объявление**
>> `DELETE /ads/id/`

> **Cписок всех категорий**
>> `GET /cats/`  
> Доступна фильтрация по названию:  
> `GET /cat/?search=кот` (ищет все вхождения 'кот' в любом регистре) либо  
> `GET /cat/?search=кот&search=песик` (ищет все вхождения 'кот' ЛИБО 'песик' в любом регистре)
> Доступна сортировка:  
> 'GET /cat/?ordering=name' - сортировка по полю name по возрастанию  
> 'GET /cat/?ordering=-name' - сортировка по полю name по убыванию
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
>> `GET /cats/id/`
> ```json
>    {
>        "pk": 1,
>        "name": "Котики"
>    }
> ```

> **Добавить категорию**
>> `POST /cats/`
> ```json
>    {
>        "name": "Котики"
>    }
> ```


> **Изменить категорию**
>> `PATCH /cats/id/`
> ```json
>    {
>        "name": "Котики"
>    }
> ```

> **Удалить категорию**
>> `DELETE /cats/id/`


> **Cписок всех пользователей (возможна пагинация)**
>> `GET /users/`
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
>> `GET /users/id/`
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
>> `POST /users/`

> **Изменить пользователя**
>> `PATCH /users/id/`

> **Удалить пользователя**
>> `DELETE /users/id/`


> **Cписок всех локаций (возможна пагинация)**
>> `GET /locations/`
> ```json
> [
>   {
>       "id": 1,
>       "name": "Москва"
>   },
>  {
>       "id": 2,
>       "name": "Питер"
>  }
> ]
> ```

> **Локация с указанным ID**
>> `GET /locations/id/`
> ```json
> {
>    "id": 1,
>    "name": "Москва"
> }
> ```

> **Добавить локацию**
>> `POST /locations/`

> **Изменить локацию**
>> `PATCH /locations/id/`

> **Удалить локацию**
>> `DELETE /locations/id/`


> **Cписок всех подборок (возможна пагинация)**
>> `GET /selections/`

> **Подборка с указанным ID**
>> `GET /selections/id/`

> **Добавить подборку**
>> `POST /selections/`

> **Изменить подборку**
>> `PATCH /selections/id/`

> **Удалить подборку**
>> `DELETE /selections/id/`



Database connection and data loading
------------
- docker-run.sh – старт контейнера с СУБД PostgreSQL
- migrate-loadall.sh – миграция структур и загрузка данных

Dependencies
------------

1. Django
2. psycopg2
