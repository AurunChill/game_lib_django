const WishListButtonOptions = {
    ADD_TO_WISHLIST: 'В желаемое',
    REMOVE_FROM_WISHLIST: 'Убрать из желаемого'
}

/**
 * Handles click event on the wishlist button
 * @param {string} user_id - The ID of the user
 * @param {string} game_id - The ID of the game
 * @param {string} is_authenticated - Flag indicating if user is authenticated
 */
function handle_btn_wishlist_click(user_id, game_id, is_authenticated) {
    if (is_authenticated === 'False') {
        console.log('here')
        window.location.href = '/accounts/login/'; 
        return;
    }

    let button = document.querySelector('#wishlist_btn');
    let in_wish_text = document.querySelector('.text_in_wishlist')
    console.log(in_wish_text)

    let is_adding = updateWishListButtonText(button, in_wish_text);

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    if (is_adding) {
        sendRequest('/add_to_wishlist/', 'POST', csrftoken, user_id, game_id)
    } else {
        sendRequest('/remove_from_wishlist/', 'POST', csrftoken, user_id, game_id)
    }
}

/**
 * Updates the text on the wishlist button and returns whether it is adding to wishlist or removing from wishlist
 * @param {Element} button - The wishlist button element
 * @returns {boolean} - True if adding to wishlist, False if removing from wishlist
 */
function updateWishListButtonText(button, label) {
    let is_adding = true;

    switch (button.innerText) {
        case WishListButtonOptions.ADD_TO_WISHLIST:
            is_adding = true;
            label.innerText = 'В желаемых'
            button.innerText = WishListButtonOptions.REMOVE_FROM_WISHLIST;
            break;
        case WishListButtonOptions.REMOVE_FROM_WISHLIST:
            is_adding = false;
            label.innerText = ''
            button.innerText = WishListButtonOptions.ADD_TO_WISHLIST;
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
