// Функция для обработки клика
function handleFavoriteClick(event) {
    // Ищем ближайший элемент с классом .favorite-icon
    const icon = event.target.closest('.favorite-icon');
    if (icon) {
        // Получаем необходимые атрибуты
        const goodsId = icon.getAttribute('data-goods-id');
        const url = icon.dataset.url;

        // Генерация URL
        const fullUrl = url.replace("0", goodsId);

        // Получаем CSRF-токен
        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

        // Отправляем запрос на сервер
        fetch(fullUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Переключаем класс active
                icon.classList.toggle('active');
            }
        })
        .catch(error => console.error('Ошибка:', error));
    }
}

// Добавляем обработчик события на документ
document.addEventListener('click', handleFavoriteClick);