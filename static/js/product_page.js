document.addEventListener('DOMContentLoaded', function() {
    const buttonShowMore = document.querySelector('.btn_show_more');
    const usersList = document.querySelector('.users_list_reviews');
    const reviews = Array.from(usersList.querySelectorAll('.another_user_review'));

    reviews.slice(3).forEach(review => {
        review.style.display = 'none';
    });
    buttonShowMore.addEventListener('click', function() {
        reviews.slice(3).forEach(review => {
            review.style.display = 'block';
        });
        buttonShowMore.style.display = 'none';
    });
});