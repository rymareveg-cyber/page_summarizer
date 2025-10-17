"""
Модуль для работы с OpenAI API для суммаризации текста.
"""
import os
import time
from typing import Optional
from openai import OpenAI
from openai import APIError, APIConnectionError, RateLimitError, APITimeoutError


class OpenAIModule:
    """Класс для работы с OpenAI API."""
    
    def __init__(self, api_key: Optional[str] = None, max_retries: int = 3):
        """
        Инициализация клиента OpenAI.
        
        Args:
            api_key: API ключ OpenAI (если не указан, берется из переменной окружения)
            max_retries: Максимальное количество попыток при ошибках
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API ключ не найден. Укажите OPENAI_API_KEY в переменных окружения "
                "или передайте его при инициализации."
            )
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://openai.api.proxyapi.ru/v1",
        )
        self.max_retries = max_retries
    
    def summarize_text(self, text: str) -> str:
        """
        Суммаризирует текст с помощью GPT-4o.
        
        Args:
            text: Текст для суммаризации
            
        Returns:
            Резюме текста в 3-5 предложениях
            
        Raises:
            ValueError: Если текст пустой
            APIError: При ошибках API после всех попыток
        """
        if not text or not text.strip():
            raise ValueError("Текст для суммаризации не может быть пустым")
        
        prompt = (
            "Ты аналитик. Сформулируй суть текста в 3–5 предложениях. "
            "Будь точным и лаконичным."
        )
        
        for attempt in range(self.max_retries):
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": text}
                    ],
                    temperature=0.7,
                    max_tokens=500
                )
                
                summary = response.choices[0].message.content
                if summary:
                    return summary.strip()
                else:
                    raise APIError("Пустой ответ от API")
                    
            except (APIConnectionError, APITimeoutError) as e:
                wait_time = 2 ** attempt  # Экспоненциальная задержка
                if attempt < self.max_retries - 1:
                    print(f"Ошибка соединения: {e}. Повторная попытка через {wait_time} сек...")
                    time.sleep(wait_time)
                else:
                    raise APIError(f"Не удалось подключиться к API после {self.max_retries} попыток: {e}")
            
            except RateLimitError as e:
                wait_time = 5 * (attempt + 1)
                if attempt < self.max_retries - 1:
                    print(f"Превышен лимит запросов. Ожидание {wait_time} сек...")
                    time.sleep(wait_time)
                else:
                    raise APIError(f"Превышен лимит запросов после {self.max_retries} попыток: {e}")
            
            except APIError as e:
                if attempt < self.max_retries - 1:
                    wait_time = 2 ** attempt
                    print(f"Ошибка API: {e}. Повторная попытка через {wait_time} сек...")
                    time.sleep(wait_time)
                else:
                    raise APIError(f"Ошибка API после {self.max_retries} попыток: {e}")
        
        raise APIError("Не удалось получить резюме после всех попыток")


def summarize_text(text: str) -> str:
    """
    Удобная функция для быстрой суммаризации текста.
    
    Args:
        text: Текст для суммаризации
        
    Returns:
        Резюме текста в 3-5 предложениях
    """
    module = OpenAIModule()
    return module.summarize_text(text)

