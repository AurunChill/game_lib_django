const api_url = 'http://127.0.0.1:8000/api/v1/comments/';

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = $.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function formatDateString(dateString) {
    // Parse the input date string to a Date object
    const date = new Date(dateString);
    
    // Function to pad single-digit numbers with a leading zero
    const pad = (num) => num.toString().padStart(2, '0');
    
    // Extract date and time components
    const year = date.getFullYear();
    const month = pad(date.getMonth() + 1); // getMonth() is zero-based, hence the +1
    const day = pad(date.getDate());
    const hours = pad(date.getHours());
    const minutes = pad(date.getMinutes());
    
    // Construct the desired output
    return `${year}-${month}-${day} ${hours}:${minutes}`;
  }


$(document).ready(function() {
    let url = window.location.href;
    let urlSegments = url.split('/');
    let nonEmptySegments = urlSegments.filter(function(segment) {
        return segment.trim() !== '';
    });
    let game_id = parseInt(nonEmptySegments[nonEmptySegments.length - 1]);

    $.ajax({
        url: api_url + `?page=1&game_id=${game_id}`,
        method: 'GET',
        success: function(response) {
            console.log(response)
            response.results.forEach((message) => {
                generate_comment(
                    message.user.image, message.user.username,
                    message.text, formatDateString(message.date)
                );
            })
        },
        error: function(error) {
            // if (error.status == 403) {
            //     window.location.href = '/accounts/login/';
            // }
        }
    });
});


$('#send_comment_form').on('submit', function(e) {
    e.preventDefault();

    const game_id = $(this).data('game_id');
    const user_id = $(this).data('user_id');
    const user_image_url = $(this).data('user_image_url');
    const user_name = $(this).data('user_name');
    const text = $(this).find('textarea').val();
    const csrftoken = getCookie('csrftoken');

    console.log(game_id, user_id, user_image_url, user_name, text, csrftoken);

    $(this).find('textarea').val('');

    $.ajax({
        url: api_url,
        method: 'POST',
        data: {
            'user_id': user_id,
            'game_id': game_id,
            'text': text
        },
        headers: {
            'X-CSRFToken': csrftoken
        },
        success: function(response) {
            console.log(response)
            generate_comment(user_image_url, user_name, text, response.date);
        },
        error: function(error) {
            if (error.status == 403) {
                window.location.href = '/accounts/login/';
            }
        }
    });
});

function generate_comment(image_url, user_name, text, date) {
    let image = null
    if (image_url === null) {
        image = `
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
            class="p-[6px] text-white bg-gray-500 stroke-current">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
        </svg>
        `;
    } else {
        image = `
        <img id="preview" class="relative object-cover rounded-md"
        src="${image_url}"
        >`;
    }
    const formatted_date = formatDateString(date);

    const template = `
<div class="bg-white p-4 rounded-lg shadow-md">
    <div class="flex items-center gap-3">
        <div class="relative h-12 w-12 my-2 self-center overflow-hidden">
            ${image}
        </div>
        <h3 class="text-lg font-bold">${user_name}</h3>
    </div>
    <p class="text-gray-700 text-sm mb-2">${formatted_date}</p>
    <p class="text-gray-700">${text}</p>
</div>
    `

    $('#comments_container').prepend(template);
}