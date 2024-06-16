const api_url = 'http://127.0.0.1:8000/api/v1/comments/';

let page_comments = []
let replying_to = null
let comment_page = 1


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


function get_comment_by_id(id) {
    for (let comment of page_comments) {
        if (comment['id'] === id) {
            return comment;
        }
    }
    return null;
}


$(document).ready(function () {
    let url = window.location.href;
    let urlSegments = url.split('/');
    let nonEmptySegments = urlSegments.filter(function (segment) {
        return segment.trim() !== '';
    });
    let game_id = parseInt(nonEmptySegments[nonEmptySegments.length - 1]);

    $.ajax({
        url: api_url + `?page=${comment_page}&game_id=${game_id}`,
        method: 'GET',
        success: function (response) {
            page_comments = response.results;
            response.results.forEach((comment, i) => {
                generate_comment(
                    i, comment.user.image, comment.user.username,
                    comment.text, formatDateString(comment.date),
                    get_comment_by_id(comment.reply_to)
                );
            });
        },
        error: function (error) {
        }
    });
});


function load_comments() {
    let url = window.location.href;
    let urlSegments = url.split('/');
    let nonEmptySegments = urlSegments.filter(function (segment) {
        return segment.trim() !== '';
    });
    let game_id = parseInt(nonEmptySegments[nonEmptySegments.length - 1]);
    comment_page++;

    $.ajax({
        url: api_url + `?page=${comment_page}&game_id=${game_id}`,
        method: 'GET',
        success: function (response) {
            page_comments.push(...response.results);
            response.results.forEach((comment, i) => {
                generate_comment(
                    i, comment.user.image, comment.user.username,
                    comment.text, formatDateString(comment.date),
                    get_comment_by_id(comment.reply_to)
                );
            });
        },
        error: function (error) {
            if (error.status == 404) {
                comment_page--;
            }
        }
    });
}


$('#send_comment_form').on('submit', function (e) {
    e.preventDefault();

    const game_id = $(this).data('game_id');
    const user_id = $(this).data('user_id');
    const user_image_url = $(this).data('user_image_url');
    const user_name = $(this).data('user_name');
    const text = $(this).find('textarea').val();
    const csrftoken = getCookie('csrftoken');

    $(this).find('textarea').val('');

    $.ajax({
        url: api_url,
        method: 'POST',
        data: {
            'user_id': user_id,
            'game_id': game_id,
            'text': text,
            'reply_to': replying_to === null ? null : page_comments[replying_to]['id']
        },
        headers: {
            'X-CSRFToken': csrftoken
        },
        success: function (response) {
            page_comments.push(response)

            generate_comment(
                page_comments.length - 1, user_image_url,
                user_name, text, response.date,
                get_comment_by_id(response.reply_to),
                false
            );
        },
        error: function (error) {
            if (error.status == 403) {
                window.location.href = '/accounts/login/';
            }
        }
    });
});


function generate_image(image_url) {
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
    return image
}


function generate_comment(
    index, image_url, user_name, 
    text, date, inner_msg, is_appending = true) {
    let image = generate_image(image_url)
    const formatted_date = formatDateString(date);

    let delete_message = `
        <div class='h-6 w-6 cursor-pointer' onclick='delete_comment(${index})'>
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
                <g id="SVGRepo_iconCarrier">
                    <path d="M10 12V17" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    </path>
                    <path d="M14 12V17" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    </path>
                    <path d="M4 7H20" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    </path>
                    <path d="M6 10V18C6 19.6569 7.34315 21 9 21H15C16.6569 21 18 19.6569 18 18V10" stroke="#000000"
                        stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>
                    <path d="M9 5C9 3.89543 9.89543 3 11 3H13C14.1046 3 15 3.89543 15 5V7H9V5Z" stroke="#000000"
                        stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>
                </g>
            </svg>
        </div>
    `

    let reply_message = null
    if (inner_msg !== null) {
        reply_message = `
        <div class="bg-white p-4 rounded-lg shadow-md mb-4">
            <div class="flex items-center gap-3">
                <div class="relative h-8 w-8 my-2 self-center overflow-hidden">
                    ${generate_image(inner_msg.user.image)}
                </div>
                <h3 class="text-md font-bold">${inner_msg.user.username}</h3>
            </div>
            <p class="text-gray-700 text-[10px] mb-2">${formatDateString(inner_msg.date)}</p>
            <p class="text-gray-700 text-xs">${inner_msg.text.length > 100 ? inner_msg.text.slice(0, 100) + '...' : inner_msg.text}</p>
        </div>
            `
    }

    const template = `
<div id="${index}" class="bg-white p-4 rounded-lg shadow-md mt-4">
    <div class="flex items-center gap-3">
        <div class="relative h-12 w-12 my-2 self-center overflow-hidden">
            ${image}
        </div>
        <h3 class="text-lg font-bold">${user_name}</h3>
        ${is_staff ? delete_message : ''}
    </div>
    <p class="text-gray-700 text-sm mb-2">${formatted_date}</p>
    ${reply_message ? reply_message : ''}
    <p class="text-gray-700">${text}</p>
    <button class='flex items-center mt-4 cursor-pointer' onclick="reply_to_comment(${index})">
            <p class="text-gray-600 text-sm">Ответить</p>
            <div class='h-4 w-4 mt-1 ms-1 cursor-pointer'>
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                    <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
                    <g id="SVGRepo_iconCarrier">
                        <path fill-rule="evenodd" clip-rule="evenodd"
                            d="M19.5 6.25C19.9142 6.25 20.25 6.58579 20.25 7C20.25 9.24444 19.298 10.7196 18.0632 11.6087C16.8667 12.4702 15.4534 12.75 14.5 12.75L6.31066 12.75L10.0303 16.4697C10.3232 16.7626 10.3232 17.2374 10.0303 17.5303C9.73744 17.8232 9.26256 17.8232 8.96967 17.5303L3.96967 12.5303C3.67678 12.2374 3.67678 11.7626 3.96967 11.4697L8.96967 6.46967C9.26256 6.17678 9.73744 6.17678 10.0303 6.46967C10.3232 6.76256 10.3232 7.23744 10.0303 7.53033L6.31066 11.25L14.5 11.25C15.2133 11.25 16.3 11.0298 17.1868 10.3913C18.0353 9.7804 18.75 8.75556 18.75 7C18.75 6.58579 19.0858 6.25 19.5 6.25Z"
                            fill="#4b5563">
                        </path>
                    </g>
                </svg>
            </div>
    </button>
</div>
    `

    if (replying_to !== null) {
        cancell_replying();
    }

    if (is_appending) {
        $('#comments_container').append(template);
    } else {
        $('#comments_container').prepend(template);
    }
}


function reply_to_comment(id) {
    replying_to = id;
    $('#cancell_replying').removeClass('hidden');
    $('#cancell_replying').addClass('flex');

    let comment = page_comments[id];
    $('#reply_text').text(`Ответить на комментарий пользователя ${comment.user.username}`);

    let comment_form_offset = $('#send_comment_form').offset().top;
    $('html, body').animate({
        scrollTop: comment_form_offset
    }, 1000);
}


function cancell_replying() {
    $('#cancell_replying').removeClass('flex');
    $('#cancell_replying').addClass('hidden');
    replying_to = null;
}



// Function to send DELETE request
function delete_comment(index) {
    let comment = page_comments[index];
    // URL assumes an endpoint like /comments//, adjust according to your routing

    fetch(api_url + `${comment['id']}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'), // Assuming you're using CSRF tokens with Django
        },
    })
    .then(response => {
        if (response.ok) {
            console.log('Deletion successful');
            $(`#${index}`).remove(); // Using jQuery to remove the element from the DOM
        } else {
            console.error('Deletion failed');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}