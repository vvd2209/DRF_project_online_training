DRF_project + Docker
24.1 Вьюсеты и дженерики
Задание 1
Создан новый Django-проект, подключен DRF и внесены все необходимые настройки.

Задание 2
Создана модель Пользователя:

все поля от обычного пользователя, но авторизацию заменена на email;
телефон;
город;
аватарка. Создана модель Курс:
название,
превью (картинка),
описание. Создана модель Урок:
название,
описание,
превью (картинка),
ссылка на видео.
Задание 3
Описана CRUD для моделей курса и урока, для курса через ViewSets, а для урока — через Generic-классы.

Для работы контроллеров описаны простейшие сериализаторы.

Работа каждого эндпоинта проверена с помощью Postman.

24.2 Сериализаторы
Задание 1
Для модели курса добавлена в сериализатор поле вывода количества уроков.

Задание 2
Добавлена новая модель «Платежи» со следующими полями:

пользователь,
дата оплаты,
оплаченный курс или урок,
сумма оплаты,
способ оплаты: наличные или перевод на счет. Для заполнения базы данных "Платежи" необходимо запустить файл fill.py, вызвав команду в терминале python manage.py fill
Задание 3
Для сериализатора модели курса реализовано поле вывода уроков.

Задание 4
Настроена фильтрация для эндпоинтов вывода списка платежей с возможностями:

порядок сортировки по дате оплаты,
фильтр по курсу или уроку,
фильтр по способу оплаты.
25.1 Права доступа в DRF
Задание 1
Настроена в проекте использование JWT-авторизации и закрыты каждый эндпоинт авторизацией.

Задание 2
Заведена группа модераторов и описана для нее права работы с любыми уроками или курсами, но без возможности их удалять и создавать новые. Заложен функционал такой проверки в контроллеры.

Задание 3
Описаны права доступа для объектов таким образом, чтобы пользователи, которые не входят в группу модераторов, могли видеть и редактировать только свои курсы и уроки.

25.2 Валидаторы, пагинация и тесты
Задание 1
Для сохранения уроков и курсов реализованы дополнительные проверки на отсутствие в материалах ссылок на сторонние ресурсы, кроме youtube.com.

Задание 2
Добавлена модель подписки на обновления курса для пользователя.

Реализован эндпоинт для установки подписки пользователя и на удаление подписки у пользователя.

Задание 3
Реализована пагинация для вывода всех уроков и курсов.

Задание 4
Написаны тесты, которые будут проверять корректность работы CRUD уроков и функционал работы подписки на обновления курса.

26.1 Документирование и безопасность
Задание 1
Подключены и настроены вывод документации для проекта.

Задание 2
Подключена возможность оплаты курсов через https://stripe.com/docs/api.

Пройдена регистрация по адресу https://dashboard.stripe.com/register.

Для работы с запросами вам понадобится реализовать обращение к эндпоинтам: https://stripe.com/docs/api/payment_intents/create — создание платежа; https://stripe.com/docs/api/payment_intents/retrieve — получение платежа.

Для тестирования можно использовать номера карт из документации: https://stripe.com/docs/terminal/references/testing#standard-test-cards

26.2. Celery
Задание 1
Настроен проект для работы с Celery, настроен celery-beat для выполнения последующих задач.

Задание 2
Добавлена асинхронная рассылка писем пользователям об обновлении материалов курса.

27.2. Docker Compose
Задачи
Описан Dockerfile для запуска контейнера с проектом.
Обернут в Docker Compose Django-проект с БД PostgreSQL.
Дописаны в docker-compose.yaml работу с Redis.
Дописаны в docker-compose.yaml работу с Celery.
Команды
Собрать образ командой docker-compose build
<<<<<<< HEAD
Запустить контейнеры командой docker-compose up
=======
Запустить контейнеры командой docker-compose up
>>>>>>> origin/main
