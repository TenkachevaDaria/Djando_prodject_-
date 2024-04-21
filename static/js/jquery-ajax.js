// Когда html документ готов (прорисован)
$(document).ready(function () {

    // Ловим собыитие клика по кнопке добавить в корзину
    $(document).on("click", ".add-to-basket", function (e) {
        // Блокируем его базовое действие
        e.preventDefault();

        // Берем элемент счетчика в значке корзины и берем оттуда значение
        var productsInCartCount = $("#products-in-basket-count");
        var basketCount = parseInt(productsInCartCount.text() || 0);

        // Получаем id товара из атрибута data-product-id
        var product_id = $(this).data("product-id");

        // Из атрибута href берем ссылку на контроллер django
        var add_to_basket_url = $(this).attr("href");

        // делаем post запрос через ajax не перезагружая страницу
        $.ajax({
            type: "POST",
            url: add_to_basket_url,
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Увеличиваем количество товаров в корзине (отрисовка в шаблоне)
                basketCount++;
                productsInCartCount.text(basketCount);

                // Меняем содержимое корзины на ответ от django (новый отрисованный фрагмент разметки корзины)
                var basketItemsContainer = $("#basket-items-container");
                basketItemsContainer.html(data.basket_items_html);

            },
        });
    });

    // Ловим собыитие клика по кнопке удалить товар из корзины
    $(document).on("click", ".remove-from-basket", function (e) {
        // Блокируем его базовое действие
        e.preventDefault();

        // Берем элемент счетчика в значке корзины и берем оттуда значение
        var productsInCartCount = $("#products-in-basket-count");
        var basketCount = parseInt(productsInCartCount.text() || 0);

        // Получаем id корзины из атрибута data-basket-id
        var basket_id = $(this).data("basket-id");
        // Из атрибута href берем ссылку на контроллер django
        var remove_from_basket = $(this).attr("href");

        // делаем post запрос через ajax не перезагружая страницу
        $.ajax({

            type: "POST",
            url: remove_from_basket,
            data: {
                basket_id: basket_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Уменьшаем количество товаров в корзине (отрисовка)
                basketCount -= data.quantity_deleted;
                productsInCartCount.text(basketCount);

                // Меняем содержимое корзины на ответ от django (новый отрисованный фрагмент разметки корзины)
                var basketItemsContainer = $("#basket-items-container");
                basketItemsContainer.html(data.basket_items_html);

            },
        });
    });




    // Теперь + - количества товара 
    // Обработчик события для уменьшения значения
    $(document).on("click", ".decrement", function () {
        // Берем ссылку на контроллер django из атрибута data-basket-change-url
        var url = $(this).data("basket-change-url");
        // Берем id корзины из атрибута data-basket-id
        var basketId = $(this).data("basket-id");
        // Ищем ближайшеий input с количеством 
        var $input = $(this).closest('.item__counter_box').find('.number');
        // Берем значение количества товара
        var currentValue = parseInt($input.val());
        // Если количества больше одного, то только тогда делаем -1
        if (currentValue > 1) {
            $input.val(currentValue - 1);
            // Запускаем функцию определенную ниже
            // с аргументами (id карты, новое количество, количество уменьшилось или прибавилось, url)
            updateCart(basketId, currentValue - 1, -1, url);
        }
    });

    // Обработчик события для увеличения значения
    $(document).on("click", ".increment", function () {
        // Берем ссылку на контроллер django из атрибута data-basket-change-url
        var url = $(this).data("basket-change-url");
        // Берем id корзины из атрибута data-basket-id
        var basketId = $(this).data("basket-id");
        // Ищем ближайшеий input с количеством 
        var $input = $(this).closest('.item__counter_box').find('.number');
        // Берем значение количества товара
        var currentValue = parseInt($input.val());

        $input.val(currentValue + 1);

        // Запускаем функцию определенную ниже
        // с аргументами (id карты, новое количество, количество уменьшилось или прибавилось, url)
        updateCart(basketId, currentValue + 1, 1, url);
    });

    function updateCart(basketId, quantity, change, url) {
        $.ajax({
            type: "POST",
            url: url,
            data: {
                basket_id: basketId,
                quantity: quantity,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },

            success: function (data) {
                // Изменяем количество товаров в корзине
                var productsInCartCount = $("#products-in-basket-count");
                var basketCount = parseInt(productsInCartCount.text() || 0);
                basketCount += change;
                productsInCartCount.text(basketCount);

                // Меняем содержимое корзины
                var basketItemsContainer = $("#basket-items-container");
                basketItemsContainer.html(data.basket_items_html);
            },
        });
    }
});