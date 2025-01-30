## 📌 О проекте
**Miko** – это веб-приложение для автоматизации процессов кафе. Оно позволяет сотрудникам быстро оформлять заказы, отслеживать их статус.

## 🚀 Функционал
- 📋 **Создание и управление заказами**
- 📌 **Отслеживание статуса заказов**
- 💵 **Высчитывать выручку за смену**

## 🛠️ Технологии
- **Backend**: Django
- **Frontend**: HTML/CSS (No JS😎)
- **База данных**: PostgreSQL

## 🔧 Установка и запуск
**Требуется установленный docker!**
1. Клонируем репозиторию в рабочую папку
```sh
git clone https://github.com/VanilCitatka/miko.git
cd miko
```

2. Требуется передать список переменных окружения (например через .env файл)

``` sh
touch .env
nano .env
```

Список переменных окружения:
- DEBUG
- POSTGRES_DB_NAME
- POSTGRES_DB_USER
- POSTGRES_DB_PASSWORD
- POSTGRES_DB_HOST
- POSTGRES_DB_PORT

3. Запустить docker-compose:
```sh
 docker compose -f 'compose.yaml' up -d --build
```

>Приложение будет доступно по адресу: localhost:8000
