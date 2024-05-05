document.addEventListener("DOMContentLoaded", function() {
    // Находим кнопку "Добавить способ оплаты"
    var addPaymentMethodBtn = document.querySelector('.save_payment_method_btn');

    // Находим панель с формой добавления способа оплаты
    var addPaymentMethodPopup = document.querySelector('.popup_user_add_payment_method');

    // Находим кнопку для закрытия панели
    var hidePopupBtn = document.querySelector('.hide_popup_add_payment_method');

    // Назначаем обработчик события клика на кнопку "Добавить способ оплаты"
    addPaymentMethodBtn.addEventListener('click', function(event) {
        // Предотвращаем отправку формы
        event.preventDefault();
        // Показываем панель с формой добавления способа оплаты
        addPaymentMethodPopup.style.display = 'block';
    });

    // Назначаем обработчик события клика на кнопку для закрытия панели
    hidePopupBtn.addEventListener('click', function() {
        // Скрываем панель с формой добавления способа оплаты
        addPaymentMethodPopup.style.display = 'none';
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const userProducts = document.querySelector('.user_products');
    const popupUserProducts = document.querySelector('.popup_user_products_history');
    const hidePopupButton = popupUserProducts.querySelector('.hide_popup_user_products_history');
    function openPopup() {
        popupUserProducts.style.display = 'block';
    }
    function closePopup() {
        popupUserProducts.style.display = 'none';
    }
    userProducts.addEventListener('click', openPopup);
    hidePopupButton.addEventListener('click', closePopup);
});

document.addEventListener("DOMContentLoaded", function() {
    const userProducts = document.querySelector('.user_products_liked');
    const popupUserProducts = document.querySelector('.popup_user_products_liked');
    const hidePopupButton = popupUserProducts.querySelector('.hide_popup_user_products_liked');
    function openPopup() {
        popupUserProducts.style.display = 'block';
    }
    function closePopup() {
        popupUserProducts.style.display = 'none';
    }
    userProducts.addEventListener('click', openPopup);
    hidePopupButton.addEventListener('click', closePopup);
});

document.addEventListener("DOMContentLoaded", function() {
    const userProducts = document.querySelector('.user_history_bought_box');
    const popupUserProducts = document.querySelector('.popup_user_purchase_history');
    const hidePopupButton = popupUserProducts.querySelector('.hide_popup_user_purchase_history');
    function openPopup() {
        popupUserProducts.style.display = 'block';
    }
    function closePopup() {
        popupUserProducts.style.display = 'none';
    }
    userProducts.addEventListener('click', openPopup);
    hidePopupButton.addEventListener('click', closePopup);
});