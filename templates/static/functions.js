

function submitURLForm() {
    let formGroup = document.getElementById('form-group')
    let urlForm = document.getElementById('url-form')
    formGroup.style.display = 'none'
    // formGroup.innerHTML = "<h2>Hola, " + urlForm.elements["url"] + ". Preparant la teva cita amb la ciència...</h2>"

    let formData = new FormData(urlForm);
    let requestOptions = {
        method: 'POST',
        redirect: 'follow',
        body: formData,
    };
    fetch('/submit_upload_business', requestOptions)
        .then(response => response.text())
        .then(data => {
            document.getElementById('convocatories').innerHTML = data;
        });
    // formGroup.innerHTML = "<h2>Llest! Tria la convocatòria a la que vulguis aplicar.<\h2>"
}


function submitWhichCall() {
    let callValue = document.querySelector('input[name="conv_select"]:checked').value;
    let urlForm = document.getElementById('url-form')
    let formData = new FormData(urlForm);
    formData.append("selected_form", callValue)
    let requestOptions = {
        method: 'POST',
        redirect: 'follow',
        body: formData,
    };
    fetch('/fill_selected_call', requestOptions)
        .then(response => response.text())
        .then(data => {
            document.getElementById('convocatories').innerHTML = data;
        });
}