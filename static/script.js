// Обработка формы суммаризации
document.getElementById('summarizeForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const urlInput = document.getElementById('urlInput');
    const submitBtn = document.getElementById('submitBtn');
    const btnText = submitBtn.querySelector('.btn-text');
    const loader = submitBtn.querySelector('.loader');
    const resultSection = document.getElementById('result');
    const errorSection = document.getElementById('error');
    const summaryBox = document.getElementById('summaryBox');
    const urlDisplay = document.getElementById('urlDisplay');
    const errorMessage = document.getElementById('errorMessage');
    
    const url = urlInput.value.trim();
    
    // Скрываем предыдущие результаты
    resultSection.style.display = 'none';
    errorSection.style.display = 'none';
    
    // Показываем загрузку
    submitBtn.disabled = true;
    btnText.style.display = 'none';
    loader.style.display = 'inline-block';
    
    try {
        const response = await fetch('/summarize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Показываем результат
            urlDisplay.textContent = `📄 ${data.url}`;
            summaryBox.textContent = data.summary;
            resultSection.style.display = 'block';
            
            // Плавная прокрутка к результату
            resultSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        } else {
            // Показываем ошибку
            errorMessage.textContent = data.error || 'Произошла ошибка при обработке страницы';
            errorSection.style.display = 'flex';
            errorSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    } catch (error) {
        // Показываем ошибку сети
        errorMessage.textContent = `Ошибка соединения: ${error.message}`;
        errorSection.style.display = 'flex';
        errorSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } finally {
        // Скрываем загрузку
        submitBtn.disabled = false;
        btnText.style.display = 'inline';
        loader.style.display = 'none';
    }
});

// Автоматическое скрытие ошибки при вводе
document.getElementById('urlInput').addEventListener('input', () => {
    document.getElementById('error').style.display = 'none';
});

