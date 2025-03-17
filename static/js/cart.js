document.addEventListener('DOMContentLoaded', function() {
    // Обработчик для добавления в корзину
    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', function() {
            const goodsId = this.getAttribute('data-goods-id');
            const url = `${window.location.origin}/users/cart/add/${goodsId}/`;
            const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

            fetch(url, {
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
                    // Скрываем кнопку
                    this.style.display = 'none';

                    // Проверяем, существует ли счетчик
                    let counter = document.getElementById(`counter-${goodsId}`);
                    if (!counter) {
                        // Создаем счетчик, если его нет
                        counter = document.createElement('div');
                        counter.id = `counter-${goodsId}`;
                        counter.className = 'counter';
                        counter.innerHTML = `
                            <button class="btn btn-primary decrease">-</button>
                            <span class="quantity">1</span>
                            <button class="btn btn-primary increase">+</button>
                        `;
                        document.getElementById(`cart-control-${goodsId}`).appendChild(counter);

                        // Добавляем обработчики для увеличения и уменьшения количества
                        const quantityElement = counter.querySelector('.quantity');
                        const decreaseButton = counter.querySelector('.decrease');
                        const increaseButton = counter.querySelector('.increase');

                        decreaseButton.addEventListener('click', function() {
                            let quantity = parseInt(quantityElement.textContent);
                            if (quantity > 1) {
                                quantity -= 1;
                                quantityElement.textContent = quantity;
                                updateCart(goodsId, quantity);
                            } else {
                                // Если количество равно 0, скрываем счетчик и показываем кнопку
                                counter.style.display = 'none';
                                let addButton = document.getElementById(`add-to-cart-${goodsId}`);
                                if (!addButton) {
                                    // Создаем кнопку, если её нет
                                    addButton = document.createElement('button');
                                    addButton.id = `add-to-cart-${goodsId}`;
                                    addButton.className = 'btn btn-primary add-to-cart';
                                    addButton.setAttribute('data-goods-id', goodsId);
                                    addButton.textContent = 'Добавить в корзину';
                                    document.getElementById(`cart-control-${goodsId}`).appendChild(addButton);

                                    // Добавляем обработчик для новой кнопки
                                    addButton.addEventListener('click', function() {
                                        const goodsId = this.getAttribute('data-goods-id');
                                        const url = `${window.location.origin}/users/cart/add/${goodsId}/`;
                                        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

                                        fetch(url, {
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
                                                // Скрываем кнопку и показываем счетчик
                                                this.style.display = 'none';
                                                const counter = document.getElementById(`counter-${goodsId}`);
                                                if (counter) {
                                                    counter.style.display = 'flex';
                                                    counter.querySelector('.quantity').textContent = 1;  // Устанавливаем начальное количество
                                                }
                                            }
                                        })
                                        .catch(error => console.error('Ошибка:', error));
                                    });
                                }
                                addButton.style.display = 'block';
                                updateCart(goodsId, 0);  // Удаляем товар из корзины
                            }
                        });

                        increaseButton.addEventListener('click', function() {
                            let quantity = parseInt(quantityElement.textContent);
                            quantity += 1;
                            quantityElement.textContent = quantity;
                            updateCart(goodsId, quantity);
                        });
                    }

                    // Показываем счетчик
                    counter.style.display = 'flex';
                    counter.querySelector('.quantity').textContent = 1;  // Устанавливаем начальное количество
                }
            })
            .catch(error => console.error('Ошибка:', error));
        });
    });

    // Обработчики для увеличения и уменьшения количества (для уже существующих счетчиков)
    document.querySelectorAll('.counter').forEach(counter => {
        const goodsId = counter.id.replace('counter-', '');
        const quantityElement = counter.querySelector('.quantity');
        const decreaseButton = counter.querySelector('.decrease');
        const increaseButton = counter.querySelector('.increase');

        decreaseButton.addEventListener('click', function() {
            let quantity = parseInt(quantityElement.textContent);
            if (quantity > 1) {
                quantity -= 1;
                quantityElement.textContent = quantity;
                updateCart(goodsId, quantity);
            } else {
                // Если количество равно 0, скрываем счетчик и показываем кнопку
                counter.style.display = 'none';
                let addButton = document.getElementById(`add-to-cart-${goodsId}`);
                if (!addButton) {
                    // Создаем кнопку, если её нет
                    addButton = document.createElement('button');
                    addButton.id = `add-to-cart-${goodsId}`;
                    addButton.className = 'btn btn-primary add-to-cart';
                    addButton.setAttribute('data-goods-id', goodsId);
                    addButton.textContent = 'Добавить в корзину';
                    document.getElementById(`cart-control-${goodsId}`).appendChild(addButton);

                    // Добавляем обработчик для новой кнопки
                    addButton.addEventListener('click', function() {
                        const goodsId = this.getAttribute('data-goods-id');
                        const url = `${window.location.origin}/users/cart/add/${goodsId}/`;
                        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

                        fetch(url, {
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
                                // Скрываем кнопку и показываем счетчик
                                this.style.display = 'none';
                                const counter = document.getElementById(`counter-${goodsId}`);
                                if (counter) {
                                    counter.style.display = 'flex';
                                    counter.querySelector('.quantity').textContent = 1;  // Устанавливаем начальное количество
                                }
                            }
                        })
                        .catch(error => console.error('Ошибка:', error));
                    });
                }
                addButton.style.display = 'block';
                updateCart(goodsId, 0);  // Удаляем товар из корзины
            }
        });

        increaseButton.addEventListener('click', function() {
            let quantity = parseInt(quantityElement.textContent);
            quantity += 1;
            quantityElement.textContent = quantity;
            updateCart(goodsId, quantity);
        });
    });

    // Функция для обновления количества товара в корзине
    function updateCart(goodsId, quantity) {
        const url = `${window.location.origin}/users/cart/update/${goodsId}/`;
        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({ quantity: quantity })
        })
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                console.error('Ошибка при обновлении корзины:', data.error);
            }
        })
        .catch(error => console.error('Ошибка:', error));
    }
});