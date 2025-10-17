# Используем официальный образ Python
FROM python:3.12

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем файлы проекта
COPY agent.py .
COPY openai_module.py .
COPY app.py .
COPY templates ./templates
COPY static ./static

# Устанавливаем переменную окружения для Python (unbuffered output)
ENV PYTHONUNBUFFERED=1

# Открываем порт для Flask
EXPOSE 5000

# По умолчанию запускаем веб-приложение
CMD ["python", "app.py"]

# Для запуска CLI версии используйте:
# docker run <image> python agent.py <URL>

