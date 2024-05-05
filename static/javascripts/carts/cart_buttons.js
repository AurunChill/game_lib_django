function remove_cart_item_list(item_id, user_id, game_id) {
    let item = document.querySelector(`.item_${item_id}`)
    if (item) {
        item.remove()
    }

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    sendRequest('/remove_from_cart/', 'POST', csrftoken, user_id, game_id)

    window.location.reload()
}

/**
 * Handles click event on the cart button
 * @param {string} user_id - The ID of the user
 * @param {string} game_id - The ID of the game
 * @param {string} is_authenticated - Flag indicating if user is authenticated
 */
function handle_btn_cart_click(user_id, game_id, is_authenticated) {
    if (is_authenticated === 'False') {
        window.location.href = '/login/';
        return;
    }

    let button = document.querySelector('#cart_btn');
    let in_cart_text = document.querySelector('.text_in_cart')

    let is_adding = updateElementsText(button, in_cart_text);

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    if (is_adding) {
        sendRequest('/add_to_cart/', 'POST', csrftoken, user_id, game_id);
    } else {
        sendRequest('/remove_from_cart/', 'POST', csrftoken, user_id, game_id);
    }
}

const CartButtonOptions = {
    REMOVE_FROM_CART: 'Убрать из корзины',
    ADD_TO_CART: 'Добавить в корзину'
}

/**
 * Updates the text on the cart button and returns whether it is adding to cart or removing from cart
 * @param {Element} button - The cart button element
 * @returns {boolean} - True if adding to cart, False if removing from cart
 */
function updateElementsText(button, label) {
    let is_adding = true;

    switch (button.innerText) {
        case CartButtonOptions.ADD_TO_CART:
            is_adding = true;
            label.innerText = 'В корзине'
            button.innerText = CartButtonOptions.REMOVE_FROM_CART;
            break;
        case CartButtonOptions.REMOVE_FROM_CART:
            is_adding = false;
            label.innerText = ''
            button.innerText = CartButtonOptions.ADD_TO_CART;
            break;
    }

    return is_adding;
}

/**
 * Sends a request to the server to add or remove a game from the cart
 * @param {string} url - The URL of the API endpoint
 * @param {string} method - The HTTP method (e.g., POST)
 * @param {string} csrftoken - The CSRF token
 * @param {string} user_id - The ID of the user
 * @param {string} game_id - The ID of the game
 */
function sendRequest(url, method, csrftoken, user_id, game_id) {
    fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            game_id: parseInt(game_id),
            user_id: parseInt(user_id)
        }),
    }).then(response => response.json())
        .then(data => {
            console.log(data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

