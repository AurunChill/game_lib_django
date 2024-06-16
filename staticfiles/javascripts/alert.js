document.addEventListener("DOMContentLoaded", function () {
    show_alerts()
});

function show_alerts() {
    const alerts = document.querySelectorAll('.alert-message');
    alerts.forEach(function (alert, index) {
        setTimeout(() => {
            alert.style.display = 'block'; // Show alert
            setTimeout(() => {
                alert.style.display = 'none'; // Hide after 5 seconds
            }, 4500 * (index + 1));
        }, 500 * index); // To avoid showing all at the same time
    });
}