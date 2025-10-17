# Page Summarizer

Проект для автоматической суммаризации текста с веб-страниц с использованием OpenAI GPT-4o.

## 🚀 Доступны 2 интерфейса

### 1. Веб-приложение (рекомендуется)
```bash
python app.py
```
Откройте в браузере: http://localhost:8088 (или другой порт из `.env`)

### 2. Командная строка
```bash
python agent.py https://example.com
```

## Описание

Page Summarizer - это инструмент, который:
- Загружает содержимое веб-страницы по URL
- Извлекает текстовый контент
- Создает краткое резюме в 3-5 предложениях с помощью GPT-4o
- Обрабатывает ошибки сети и API с автоматическими повторными попытками
- Предоставляет современный веб-интерфейс с корпоративным дизайном

## Функционал

### Основные возможности:
- **Загрузка веб-страниц**: Использует библиотеку `requests` и `BeautifulSoup` для извлечения текста
- **Суммаризация**: Применяет GPT-4o для создания краткого резюме
- **Обработка ошибок**: Автоматические повторные попытки при сетевых ошибках
- **Типизация**: Полная типизация кода для лучшей поддержки
- **Безопасность**: API ключи хранятся в переменных окружения

### Архитектура:
- `app.py` - Flask веб-приложение
- `agent.py` - агент для загрузки и суммаризации страниц
- `openai_module.py` - модуль для работы с OpenAI API
- `templates/` - HTML шаблоны
- `static/` - CSS и JavaScript файлы
- Retry-логика с экспоненциальной задержкой
- Обработка таймаутов, ошибок соединения и лимитов API

## Требования

- Python 3.8 или выше
- API ключ OpenAI (для ProxyAPI)
- Интернет-соединение

## Конфигурация

Все настройки хранятся в файле `.env`:

```env
# API ключ для OpenAI (ProxyAPI)
OPENAI_API_KEY=your_api_key_here

# Порт для веб-приложения (по умолчанию 5000)
FLASK_PORT=8088

# Хост для веб-приложения (по умолчанию 0.0.0.0)
FLASK_HOST=0.0.0.0

# Режим отладки (True/False)
FLASK_DEBUG=True
```

Создайте файл `.env` на основе `.env.example` и укажите свои параметры.

## Установка

### Локальная установка

1. Клонируйте репозиторий:
```bash
git clone <your-repo-url>
cd page_summarizer
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Создайте файл `.env` и настройте параметры:
```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Отредактируйте `.env` и укажите свой API ключ и желаемый порт.

**Альтернатива:** Установите переменную окружения с API ключом:

**Linux/Mac:**
```bash
export OPENAI_API_KEY="ваш_api_ключ"
```

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="ваш_api_ключ"
```

**Windows (CMD):**
```cmd
set OPENAI_API_KEY=ваш_api_ключ
```

## Использование

### Веб-приложение (рекомендуется):

1. Убедитесь что `.env` файл настроен с вашим API ключом

2. Запустите сервер:
```bash
python app.py
```

3. Откройте браузер по адресу, указанному в консоли (например: http://localhost:8088)

4. Введите URL страницы и нажмите "Создать резюме"

### Командная строка:

```bash
python agent.py https://example.com
```

### Использование как библиотеки:

```python
from agent import PageSummarizerAgent

# Создание агента
agent = PageSummarizerAgent()

# Получение резюме страницы
summary = agent.summarize_page("https://example.com")
print(summary)
```

### Пример с передачей API ключа в коде:

```python
from agent import PageSummarizerAgent

agent = PageSummarizerAgent(api_key="ваш_api_ключ")
summary = agent.summarize_page("https://example.com")
```

## Docker

### Сборка Docker образа:

```bash
docker build -t <dockerhub_username>/page_summarizer .
```

Например:
```bash
docker build -t myusername/page_summarizer .
```

### Запуск контейнера:

**Веб-приложение (по умолчанию):**
```bash
docker run -p 5000:5000 -e OPENAI_API_KEY="ваш_api_ключ" <dockerhub_username>/page_summarizer
```
Откройте http://localhost:5000

**Командная строка:**
```bash
docker run -e OPENAI_API_KEY="ваш_api_ключ" <dockerhub_username>/page_summarizer python agent.py https://example.com
```

### Публикация образа в Docker Hub:

1. Войдите в Docker Hub:
```bash
docker login
```

2. Загрузите образ:
```bash
docker push <dockerhub_username>/page_summarizer
```

Например:
```bash
docker push myusername/page_summarizer
```

3. Теперь образ доступен публично и может быть загружен другими:
```bash
docker pull <dockerhub_username>/page_summarizer
```

### Примеры использования Docker:

**Веб-приложение:**
```bash
docker run -p 5000:5000 -e OPENAI_API_KEY="your_key" myusername/page_summarizer
```

**CLI с конкретным URL:**
```bash
docker run -e OPENAI_API_KEY="your_key" myusername/page_summarizer python agent.py https://en.wikipedia.org/wiki/Python
```

**С .env файлом:**
```bash
docker run -p 5000:5000 --env-file .env myusername/page_summarizer
```

## Обработка ошибок

Проект корректно обрабатывает следующие ошибки:

- **Сетевые ошибки**: Автоматические повторные попытки с экспоненциальной задержкой
- **Таймауты**: Настраиваемый таймаут для HTTP запросов
- **Ошибки API**: Повторные попытки при временных ошибках
- **Rate Limiting**: Автоматическое ожидание при превышении лимита запросов
- **Невалидные URL**: Валидация входных данных
- **Пустые страницы**: Проверка наличия текстового контента

## Конфигурация

### Настройки агента:

```python
agent = PageSummarizerAgent(
    api_key="ваш_ключ",  # Опционально, можно использовать переменную окружения
    timeout=10           # Таймаут HTTP запросов в секундах
)
```

### Настройки OpenAI модуля:

```python
from openai_module import OpenAIModule

module = OpenAIModule(
    api_key="ваш_ключ",  # Опционально
    max_retries=3        # Количество повторных попыток
)
```

## Структура проекта

```
page_summarizer/
├── agent.py              # Основной агент
├── openai_module.py      # Модуль работы с OpenAI
├── requirements.txt      # Зависимости Python
├── README.md            # Документация
├── Dockerfile           # Docker конфигурация
└── .gitignore          # Игнорируемые файлы
```

## Лицензия

MIT License

## Поддержка

При возникновении проблем создайте issue в репозитории проекта.

