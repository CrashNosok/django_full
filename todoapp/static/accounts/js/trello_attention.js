function validateMyForm() {
    let field_key = document.getElementById('id_trello_api_key').value;
    let field_secret = document.getElementById('id_trello_api_secret').value;
    if (field_key.length && field_key.length != 32 || field_secret.length && field_secret.length != 64) {
        alert('your api key mast have 32 simbols\nyour api secret mast have 32 simbols');
        return false;
    }
    if ((initial_length_key != 32 && initial_length_secret != 64) && (field_key.length || field_secret.length)) {
        let answer = confirm('if you');
        if (!answer) {
            return false;
        }
    }
    return true;
}


let initial_length_key = document.getElementById('id_trello_api_key').value.length;
let initial_length_secret = document.getElementById('id_trello_api_secret').length;


