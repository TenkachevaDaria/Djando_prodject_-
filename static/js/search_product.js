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