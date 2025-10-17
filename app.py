"""
Веб-приложение для суммаризации текста с веб-страниц.
"""
from flask import Flask, render_template, request, jsonify
from agent import PageSummarizerAgent
from dotenv import load_dotenv
import os

# Загрузка переменных из .env файла
load_dotenv()

app = Flask(__name__)

# Инициализация агента
agent = PageSummarizerAgent()


@app.route('/')
def index():
    """Главная страница."""
    return render_template('index.html')


@app.route('/summarize', methods=['POST'])
def summarize():
    """API endpoint для суммаризации."""
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({
                'success': False,
                'error': 'URL не может быть пустым'
            }), 400
        
        if not url.startswith(('http://', 'https://')):
            return jsonify({
                'success': False,
                'error': 'URL должен начинаться с http:// или https://'
            }), 400
        
        # Получаем резюме
        summary = agent.summarize_page(url)
        
        return jsonify({
            'success': True,
            'url': url,
            'summary': summary
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    # Проверяем наличие API ключа
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠ ВНИМАНИЕ: Не установлена переменная окружения OPENAI_API_KEY")
        print("Создайте файл .env на основе .env.example или установите переменную окружения:")
        print('  Windows: $env:OPENAI_API_KEY="your_key"')
        print('  Linux/Mac: export OPENAI_API_KEY="your_key"')
        exit(1)
    
    # Получаем настройки из .env
    port = int(os.getenv('FLASK_PORT', 5000))
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"\n{'='*60}")
    print(f"  Page Summarizer запущен!")
    print(f"{'='*60}")
    print(f"  URL: http://localhost:{port}")
    print(f"  Сеть: http://{host}:{port}")
    print(f"  Режим отладки: {'Включен' if debug else 'Выключен'}")
    print(f"{'='*60}\n")
    
    app.run(debug=debug, host=host, port=port)

