let alerts = document.querySelectorAll('.alert');
for (let a of alerts) {
    a.querySelector('.close').addEventListener('click', close_alert);
}

function close_alert(e) {
    e.target.parentElement.remove();
}
