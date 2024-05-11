document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('input[name="q"]');
    const productList = document.querySelector('.products_searchers_list');
    const productItems = productList.querySelectorAll('.product_mini_card');
    const showMoreButton = document.querySelector('.drop_list__btn');

    let visibleItemCount = 5; // Количество отображаемых элементов по умолчанию
    const totalItems = productItems.length;

    function filterProducts(searchTerm) {
        let visibleItemsCount = 0;

        productItems.forEach(function(item) {
            const productName = item.querySelector('.product_name').textContent.trim().toLowerCase();
            if (productName.includes(searchTerm)) {
                if (visibleItemsCount < visibleItemCount) {
                    item.style.display = 'block';
                    visibleItemsCount++;
                } else {
                    item.style.display = 'none';
                }
            } else {
                item.style.display = 'none';
            }
        });

        if (visibleItemsCount < totalItems) {
            showMoreButton.style.display = 'block';
        } else {
            showMoreButton.style.display = 'none';
        }
    }

    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.trim().toLowerCase();
        filterProducts(searchTerm);
    });

    showMoreButton.addEventListener('click', function() {
        visibleItemCount += 5;
        const searchTerm = searchInput.value.trim().toLowerCase();
        filterProducts(searchTerm);
    });
});


const searchInput = document.querySelector('input[type="search"]');
const dropListContainer = document.querySelector('.drop_list_container');

searchInput.addEventListener('input', function() {
    if (this.value.trim() !== '') {
        dropListContainer.style.display = 'block';
    } else {
        dropListContainer.style.display = 'none';
    }
});


// мобильный
document.addEventListener('DOMContentLoaded', function() {
    const searchInputMobile = document.querySelector('input[name="q_mobile"]');
    const productListMobile = document.querySelector('.products_searchers_list_mobile');
    const productItemsMobile = productListMobile.querySelectorAll('.product_mini_card_mobile');
    const showMoreButtonMobile = document.querySelector('.drop_list__btn_mobile');

    let visibleItemCountMobile = 5;
    const totalItems_mobile = productItemsMobile.length;

    function filterProducts_mobile(searchTerm) {
        let visibleItemsCount_mobile = 0;

        productItemsMobile.forEach(function(item) {
            const productNameMobile = item.querySelector('.product_name_mobile').textContent.trim().toLowerCase();
            if (productNameMobile.includes(searchTerm)) {
                if (visibleItemsCount_mobile < visibleItemCountMobile) {
                    item.style.display = 'block';
                    visibleItemsCount_mobile++;
                } else {
                    item.style.display = 'none';
                }
            } else {
                item.style.display = 'none';
            }
        });

        if (visibleItemsCount_mobile < totalItems_mobile) {
            showMoreButtonMobile.style.display = 'block';
        } else {
            showMoreButtonMobile.style.display = 'none';
        }
    }

    searchInputMobile.addEventListener('input', function() {
        const searchTermMobile = this.value.trim().toLowerCase();
        filterProducts_mobile(searchTermMobile);
    });

    showMoreButtonMobile.addEventListener('click', function() {
        visibleItemCountMobile += 5;
        const searchTermMobile = searchInputMobile.value.trim().toLowerCase();
        filterProducts_mobile(searchTermMobile);
    });

    const dropListContainerMobile = document.querySelector('.drop_list_container_mobile');

    searchInputMobile.addEventListener('focus', function() {
        dropListContainerMobile.style.display = 'block';
    });

    searchInputMobile.addEventListener('blur', function() {
        setTimeout(function() {
            dropListContainerMobile.style.display = 'none';
        }, 100);
    });
});
