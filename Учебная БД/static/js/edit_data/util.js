function sendRequest(url, method, data) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    };

    fetch(url, options)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Ошибка HTTP: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Успех:', data);
        })
        .catch(error => {
            console.error('Ошибка:', error);
        });
}

export function calculateDiscount(amount) {
    if (amount >= 20000) {
        return 10;
    } else if (amount >= 10000) {
        return 5;
    } else {
        return 0;
    }
}

export { sendRequest };
