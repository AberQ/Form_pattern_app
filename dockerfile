FROM python:3.12-slim

# Установка необходимых пакетов
RUN apt-get update && apt-get install -y \
    gcc \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование всех файлов проекта
COPY . .

# Установка переменных окружения
ENV DJANGO_SETTINGS_MODULE=base.settings
ENV PYTHONUNBUFFERED 1

# Запуск сервера Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
