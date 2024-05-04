const WishListButtonOptions = {
    ADD_TO_WISHLIST: 'В желаемое',
    REMOVE_FROM_WISHLIST: 'Убрать из желаемого'
}

function handle_btn_wishlist_click(user_id, game_id, is_authenticated) {
    if (is_authenticated === 'False') {
        window.location.href = '/login/';
        return;
    }

    let button = document.querySelector('#wishlist_btn')
    let is_adding = true

    switch (button.innerText) {
        case WishListButtonOptions.ADD_TO_WISHLIST:
            is_adding = true
            button.innerText = WishListButtonOptions.REMOVE_FROM_WISHLIST;
            break;
        case WishListButtonOptions.REMOVE_FROM_WISHLIST:
            is_adding = false
            button.innerText = WishListButtonOptions.ADD_TO_WISHLIST;
            break;
    }
 
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    if (is_adding) {
        fetch('/add_to_wishlist/', { // Make sure to adjust the URL if necessary
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
        fetch('/remove_from_withlist/', { // Make sure to adjust the URL if necessary
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
