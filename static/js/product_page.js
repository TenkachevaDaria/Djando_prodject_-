document.addEventListener('DOMContentLoaded', function() {
    const buttonShowMore = document.querySelector('.btn_show_more');
    const usersList = document.querySelector('.users_list_reviews');
    const reviews = Array.from(usersList.querySelectorAll('.another_user_review'));

    // Показать только первые три комментария
    reviews.slice(3).forEach(review => {
        review.style.display = 'none';
    });

    // Обработчик события клика на кнопку "Смотреть ещё"
    buttonShowMore.addEventListener('click', function() {
        // Показать остальные скрытые комментарии
        reviews.slice(3).forEach(review => {
            review.style.display = 'block';
        });
        // Скрыть кнопку "Смотреть ещё"
        buttonShowMore.style.display = 'none';
    });
});