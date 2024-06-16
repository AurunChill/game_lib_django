let $burger_menu = null
let $dropdown_menu = null

$(document).ready(function () {
    $burger_menu = $('#burger_menu');
    $dropdown_menu = $('#dropdown_menu');

    $dropdown_menu.addClass('hidden');

    $burger_menu.on('click', function () {
        $dropdown_menu.toggleClass('hidden');
    });
});

$(document).on('click', function (event) {
    const $target = $(event.target);
    const is_outside_dropdown = !$dropdown_menu.has($target).length && $target[0] !== $dropdown_menu[0];
    const is_not_burger_menu = $target[0] !== $burger_menu[0];
    const does_not_have_ripple_class = !$target.hasClass('ripple');
    const is_not_svg = $target.prop('tagName').toLowerCase() !== 'svg';

    if (is_outside_dropdown && is_not_burger_menu && does_not_have_ripple_class && is_not_svg) {
        $dropdown_menu.addClass('hidden');
    }
});

function createRipple(event) {
    const $button = $(event.currentTarget);
    const $circle = $('');
    const diameter = Math.max($button.outerWidth(), $button.outerHeight());
    const radius = diameter / 2;

    $circle.css({
        width: diameter,
        height: diameter,
        left: event.clientX - $button.offset().left - radius,
        top: event.clientY - $button.offset().top - radius
    });

    $button.append($circle);

    setTimeout(() => $circle.remove(), 600); // Adjust to match the animation duration!
}