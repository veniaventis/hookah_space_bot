# Используем официальный образ Python в качестве основы
FROM python:3.12-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем все файлы проекта в контейнер
COPY . /app

# Устанавливаем зависимости (если они есть в requirements.txt)
RUN pip install --no-cache-dir -r requirements.txt

# Создаем директорию для хранения данных
RUN mkdir -p /app/data

# Устанавливаем переменную окружения для токена бота
ENV BOT_TOKEN=""

RUN which alembic

# Запускаем бота
CMD ["python", "hookah_space_bot.py"]


