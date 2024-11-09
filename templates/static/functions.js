

function submitURLForm() {
    let formGroup = document.getElementById('form-group')
    let convElement = document.getElementById('convocatories')
    let urlForm = document.getElementById('url-form')
    formGroup.style.display = 'none'
    // formGroup.innerHTML = "<h2>Hola, " + urlForm.elements["url"] + ". Preparant la teva cita amb la ciència...</h2>"

    let formData = new FormData(urlForm);
    let requestOptions = {
        method: 'POST',
        redirect: 'follow',
        body: formData,
    };
    convElement.style.display = 'block'
    convElement.innerHTML = '<div class="loader">Carregant...</div>'
    fetch('/submit_upload_business', requestOptions)
        .then(response => response.text())
        .then(data => {
            document.getElementById('convocatories').innerHTML = data;
        });
    // formGroup.innerHTML = "<h2>Llest! Tria la convocatòria a la que vulguis aplicar.<\h2>"
}


function submitWhichCall() {
    let callValue = document.querySelector('input[name="conv_select"]:checked').value;
    let convElement = document.getElementById('convocatoria_emplenada')
    let urlForm = document.getElementById('url-form')
    let formData = new FormData(urlForm);
    formData.append("selected_form", callValue)
    let requestOptions = {
        method: 'POST',
        redirect: 'follow',
        body: formData,
    };
    document.getElementById('submit_button_ok').style='display: none;'
    convElement.style.display = 'block'
    convElement.innerHTML = '<div class="loader">Carregant...</div>'
    fetch('/fill_selected_call', requestOptions)
        .then(response => response.text())
        .then(data => {
            convElement.innerHTML = data;
        });
}

function submitRevision() {

}