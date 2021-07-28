# mi-trainee-domclick-test
Тестовое задание для стажера в ДомКлик.

## Стек: 
Python 3, Django 3, SQLite, Unittest

## Описание:
CRM для регистрации и обработки заявок от клиентов.

Реализован пользовательский функционал:
*	Регистрация, сброс и изменение пароля. Редактирование профиля пользователя CRM.
*	Создание, изменение и удаление заявок.
*	Создание, изменение и удаление профиля клиента.
*	Оповещение клиента в телеграм об создании и изменении статуса заявки.
*	Фильтрация зявок по конкретной дате, промежутке дат, типу, статусу или сразу нескольким параметрам.

## Установка:
- Склонируйте проект из реппозитория на GitHub
    ```
    git clone https://github.com/wiky-avis/trainee-domclick-test.git
    ```
- Установите виртуальное окружение, затем активируйте его
    ```
    python -m venv venv
    ```
    ```
    source venv/Scripts/activate
    ```
- Установите все необходимые зависимости
    ```
    pip install -r requirements.txt
    ```
- Перейдите в директорию CRM-Project/
    ```
    cd CRM-Project
    ```
- Запустите миграции базы данных
    ```
    python manage.py migrate
    ```
- Запуск проекта
    ```
    python manage.py runserver
    ```
- Телеграм
    Для работы сервиса по отправке сообщений в телеграм клиента, нужно создать бота([Инструкция](https://marketplace.visualstudio.com/items?itemName=humao.rest-client)) который будет отправлять эти сообщения. Нужен будет токен и chat ID. Поле этого нужно создать в корневой папке проекта файл .env, а в нем две переменные TELEGRAM_TOKEN и CHAT_ID.

# Описание функционала и правила работы с сервисом

На главной странице два раздела: Клиентам и Сотрудникам.

## Клиентам:
Пользватель кликнув по ссылке "Клиентам", попадает на страницу заполнения формы заявки, где выбирает тип заявки и заполняет обязательные поля(имя, фамилия, телефон, почта). Пользователь может также указать свой телеграмм ID, чтобы получать уведомления, это поле для заполнения не обязательно. После заполнения формы и нажатия соответсвущей кнопки, заявка сохраняется в базе данных и видна только сотрудникам должность которых соответствует типу заявки.

## Сотрудникам
Пользватель кликнув по ссылке "Сотрудникам", попадает на страницу где можно зарегистрироваться и авторизороваться.

Регистрация:
Пользователь заполняет форму регистрации, после чего получает роль 'Пользователь без доступа в CRM'. Для получения доступа в CRM нужно обратиться к администратору сайта. Смена роли производится только администратором в админ панели. Доступные роли для доступа: Специалист по ремонту, Специалист по обслуживанию, Консультант. При необходимости можно добавить или изменить роли в settings.py проекта.

Авторизация:
Доступ в CRM имеют только Специалист по ремонту, Специалист по обслуживанию, Консультант или Администратор.

CRM:
На главной странице CRM пользоваитель видит список всех заявок, которые может отфильтровать по конкретной дате, промежутке дат, типу, статусу или сразу нескольким параметрам. Здесь же можно создать новую заявку, например если клиент обратился по телефону.

Страница "Мои заявки". Здесь пользователь видит только список заявок которые соответствуют его должности. Заявки также можно отфильтровать по конкретной дате, промежутке дат, статусу или сразу нескольким параметрам. Заявки можно редактировать(только менять статус: в работе, закрыта) или удалять.

Страница "Клиенты". Здесь можно увидеть всех клиентов. Создать профиль клиента, отредактировать или удалить.

Страница "Коллеги". Здесь можно увидеть всех коллег и их данные для связи.

Страница "Профиль". Здесь можно посмотреть свои данные и если необходимо, отредактировать(например сменить фото).

Далее кнопки "Изменить пароль" и "Выйти".

## Быстрая демонстрация:
[![Скринкаст сайта](/CRM-Project/images/image.jpg)](https://recordit.co/4Wrk3oaN15)

