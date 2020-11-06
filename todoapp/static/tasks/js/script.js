async function complete_task(event) {
    let checkbox = event.target;
    let task_id = checkbox.getAttribute('data-uid');
    let url = `/tasks/complete/${task_id}`;

    checkbox.setAttribute('disabled','disabled');
    checkbox.setAttribute('checked','checked');

    let response = await fetch(url);
    let text = await response.text();
    if (text == 'OK') {
        if (checkbox.classList.contains('in_progress')) {
            checkbox.classList.remove('in_progress');
        }
    }
}


let checkboxes = document.querySelectorAll('.in_progress');

for (let checkbox of checkboxes) {
    checkbox.addEventListener('click', complete_task);
}


