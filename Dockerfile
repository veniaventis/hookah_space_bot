# Используем официальный образ Python в качестве основы
FROM python:3.12-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем все файлы проекта в контейнер
COPY . /app

# Устанавливаем зависимости (если они есть в requirements.txt)
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем переменную окружения для токена бота
ENV BOT_TOKEN=""

# Запускаем бота
CMD ["python", "hookah_space_bot.py"]
