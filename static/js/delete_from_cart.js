// Скрипт для обработки удаления
$(document).ready(function() {
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    var deleteUrl;  // Переменная для хранения URL удаления
    

    // При открытии модального окна обновляем URL удаления
    $('.delete-btn').click(function() {
        deleteUrl = $(this).data('url');
    });

    // При подтверждении удаления отправляем POST-запрос
    $('#confirmDelete').click(function() {
        $.ajax({
            url: deleteUrl,
            method: 'POST',
            data: {
                csrfmiddlewaretoken: csrfToken,
            },
            success: function(response) {
                location.reload();  // Перезагружаем страницу после удаления
            },
            error: function(xhr, status, error) {
                console.error("Ошибка:", error);  // Логируем ошибку
            }
        });
    });
});