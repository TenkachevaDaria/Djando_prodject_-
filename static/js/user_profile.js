// открытие попапа с формой добавления способа оплаты
document.addEventListener("DOMContentLoaded", function() {
    var addPaymentMethodBtn = document.querySelector('.save_payment_method_btn');
    var addPaymentMethodPopup = document.querySelector('.popup_user_add_payment_method');
    var hidePopupBtn = document.querySelector('.hide_popup_add_payment_method');

    addPaymentMethodBtn.addEventListener('click', function(event) {
        event.preventDefault();
        addPaymentMethodPopup.style.display = 'block';
    });
    hidePopupBtn.addEventListener('click', function() {
        addPaymentMethodPopup.style.display = 'none';
    });
});

// открытие попапап с выставленными пользователем товарами
document.addEventListener("DOMContentLoaded", function() {
    const userProducts = document.querySelector('.user_products');
    const popupUserProducts = document.querySelector('.popup_user_products_history');
    const hidePopupButton = popupUserProducts.querySelector('.hide_popup_user_products_history');
    function openPopup() {
        popupUserProducts.style.display = 'block';
    }
    function closePopup(event) {
        event.preventDefault();
        popupUserProducts.style.display = 'none';
    }
    userProducts.addEventListener('click', openPopup);
    hidePopupButton.addEventListener('click', closePopup);
});

// открытие попапа с избранными товарами
document.addEventListener("DOMContentLoaded", function() {
    const userFavProducts = document.querySelector('.user_products_liked');
    const popupFavUserProducts = document.querySelector('.popup_user_products_liked');
    const hidePopupButton = popupFavUserProducts.querySelector('.hide_popup_user_products_liked');
    function openPopup() {
        popupFavUserProducts.style.display = 'block';
    }
    function closePopup(event) {
        event.preventDefault();
        popupFavUserProducts.style.display = 'none';
    }
    userFavProducts.addEventListener('click', openPopup);
    hidePopupButton.addEventListener('click', closePopup);
});

// открытие попапа с историей покупок
document.addEventListener("DOMContentLoaded", function() {
    const userBuyProducts = document.querySelector('.user_history_bought_box');
    const popupUserBuyProducts = document.querySelector('.popup_user_purchase_history');
    const hidePopupButton = popupUserBuyProducts.querySelector('.hide_popup_user_purchase_history');
    function openPopup() {
        popupUserBuyProducts.style.display = 'block';
    }
    function closePopup(event) {
        event.preventDefault();
        popupUserBuyProducts.style.display = 'none';
    }
    userBuyProducts.addEventListener('click', openPopup);
    hidePopupButton.addEventListener('click', closePopup);
});

// открытие попапа с редактированием выставленного товара пользователем
document.addEventListener("DOMContentLoaded", function() {
    const userChangeProducts = document.querySelectorAll('.active_user_product');
    const popupUserProducts = document.querySelector('.popup_user_products_history');
    userChangeProducts.forEach(function(product) {
        const slug = product.getAttribute('data-product-slug');
        const popupUserChangeProducts = document.getElementById('popup_' + slug);
        const hidePopupChangeButton = popupUserChangeProducts.querySelector('.hide_popup_edit_product');
        
        function openPopup() {
            popupUserChangeProducts.style.display = 'block';
            popupUserProducts.style.display = 'none';
            document.querySelector('header').style.zIndex = '1';
            document.querySelector('main').style.marginBottom = '250px';
        }
        
        function closePopup(event) {
            event.preventDefault();
            popupUserChangeProducts.style.display = 'none';
            popupUserProducts.style.display = 'block';
            document.querySelector('header').style.zIndex = '2';
            document.querySelector('main').style.marginBottom = '100px';
        }
        
        product.addEventListener('click', openPopup);
        hidePopupChangeButton.addEventListener('click', closePopup);
    });
});

const cvvHint = document.querySelector('.clue_cvv');
const cvvHintText = document.querySelector('.clue_cvv_text');
cvvHint.addEventListener('mouseover', () => {
    cvvHintText.style.display = 'block';
});
cvvHint.addEventListener('mouseleave', () => {
    cvvHintText.style.display = 'none';
});

document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('.user_input_page, #id_image');
    const submitButton = document.querySelector('.save_user_data_btn');

    inputs.forEach(function(input) {
        input.addEventListener('input', function() {
            submitButton.style.opacity = '1';
        });
    });
});