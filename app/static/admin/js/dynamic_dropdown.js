// static/admin/js/dynamic_dropdown.js
document.addEventListener('DOMContentLoaded', function () {
    const districtField = document.querySelector('#id_district');
    const marketField = document.querySelector('#id_market');

    if (districtField && marketField) {
        districtField.addEventListener('change', function () {
            const districtId = districtField.value;

            // Reset the market dropdown
            marketField.innerHTML = '<option value="">---------</option>';

            if (districtId) {
                fetch(`/get_markets/${districtId}/`)
                    .then(response => response.json())
                    .then(data => {
                        data.markets.forEach(market => {
                            const option = document.createElement('option');
                            option.value = market.id;
                            option.textContent = market.name;
                            marketField.appendChild(option);
                        });
                    })
                    .catch(error => {
                        console.error('Error fetching markets:', error);
                        alert('Failed to fetch markets. Please try again.');
                    });
            }
        });
    }
});
