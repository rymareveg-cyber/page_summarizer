"""
Агент для загрузки и суммаризации текста с веб-страниц.
"""
import sys
import requests
from typing import Optional
from bs4 import BeautifulSoup
from openai_module import OpenAIModule


class PageSummarizerAgent:
    """Агент для суммаризации содержимого веб-страниц."""
    
    def __init__(self, api_key: Optional[str] = None, timeout: int = 10):
        """
        Инициализация агента.
        
        Args:
            api_key: API ключ OpenAI (опционально)
            timeout: Таймаут для HTTP запросов в секундах
        """
        self.openai_module = OpenAIModule(api_key=api_key)
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def fetch_page_text(self, url: str) -> str:
        """
        Загружает текст с веб-страницы.
        
        Args:
            url: URL страницы для загрузки
            
        Returns:
            Текстовое содержимое страницы
            
        Raises:
            ValueError: Если URL невалидный
            requests.RequestException: При ошибках загрузки
        """
        if not url or not url.strip():
            raise ValueError("URL не может быть пустым")
        
        if not url.startswith(('http://', 'https://')):
            raise ValueError("URL должен начинаться с http:// или https://")
        
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            # Парсим HTML и извлекаем текст
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Удаляем скрипты и стили
            for script in soup(['script', 'style', 'nav', 'footer', 'header']):
                script.decompose()
            
            # Извлекаем текст
            text = soup.get_text(separator=' ', strip=True)
            
            # Убираем множественные пробелы
            text = ' '.join(text.split())
            
            if not text:
                raise ValueError("Не удалось извлечь текст со страницы")
            
            return text
            
        except requests.Timeout:
            raise requests.RequestException(f"Превышено время ожидания ({self.timeout} сек) при загрузке {url}")
        except requests.ConnectionError:
            raise requests.RequestException(f"Ошибка соединения при загрузке {url}")
        except requests.HTTPError as e:
            raise requests.RequestException(f"HTTP ошибка при загрузке {url}: {e}")
        except Exception as e:
            raise requests.RequestException(f"Неожиданная ошибка при загрузке {url}: {e}")
    
    def summarize_page(self, url: str, max_chars: int = 8000) -> str:
        """
        Загружает страницу и возвращает её резюме.
        
        Args:
            url: URL страницы для суммаризации
            max_chars: Максимальное количество символов для отправки в API
            
        Returns:
            Резюме страницы в 3-5 предложениях
        """
        try:
            print(f"Загрузка страницы: {url}")
            text = self.fetch_page_text(url)
            
            # Ограничиваем длину текста для API
            if len(text) > max_chars:
                text = text[:max_chars] + "..."
                print(f"Текст обрезан до {max_chars} символов")
            
            print(f"Получено {len(text)} символов текста")
            print("Суммаризация текста...")
            
            summary = self.openai_module.summarize_text(text)
            
            print("Резюме успешно создано!")
            return summary
            
        except ValueError as e:
            error_msg = f"Ошибка валидации: {e}"
            print(error_msg, file=sys.stderr)
            raise
        except requests.RequestException as e:
            error_msg = f"Ошибка загрузки страницы: {e}"
            print(error_msg, file=sys.stderr)
            raise
        except Exception as e:
            error_msg = f"Неожиданная ошибка: {e}"
            print(error_msg, file=sys.stderr)
            raise


def main():
    """Основная функция для запуска агента из командной строки."""
    if len(sys.argv) < 2:
        print("Использование: python agent.py <URL>")
        print("Пример: python agent.py https://example.com")
        sys.exit(1)
    
    url = sys.argv[1]
    
    try:
        agent = PageSummarizerAgent()
        summary = agent.summarize_page(url)
        
        print("\n" + "="*80)
        print("РЕЗЮМЕ:")
        print("="*80)
        print(summary)
        print("="*80)
        
    except Exception as e:
        print(f"\nОшибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

