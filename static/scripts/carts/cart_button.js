const CartButtonOptions = {
    ADD_TO_CART: 'Добавить в корзину',
    REMOVE_FROM_CART: 'Убрать из корзины'
}

function handle_btn_cart_click(user_id, game_id) {
    let button = document.querySelector('#cart_btn')
    let is_adding = true

    switch (button.innerText) {
        case CartButtonOptions.ADD_TO_CART:
            is_adding = true
            button.innerText = CartButtonOptions.REMOVE_FROM_CART;
            break;
        case CartButtonOptions.REMOVE_FROM_CART:
            is_adding = false
            button.innerText = CartButtonOptions.ADD_TO_CART;
            break;
    }
 
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    if (is_adding) {
        fetch('/add_to_cart/', { // Make sure to adjust the URL if necessary
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                game_id: parseInt(game_id),
                user_id: parseInt(user_id)
            }),
        }).then(response => response.json())
            .then(data => {
                console.log(data);
            }
            )
            .catch((error) => {
                console.error('Error:', error);
            }
        );
    } else {
        fetch('/remove_from_cart/', { // Make sure to adjust the URL if necessary
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                game_id: parseInt(game_id),
                user_id: parseInt(user_id)
            }),
        }).then(response => response.json())
            .then(data => {
                console.log(data);
            }
            )
            .catch((error) => {
                console.error('Error:', error);
            }
        );
    }
}
