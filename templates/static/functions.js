

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
    document.getElementById('submit_button_ok').display='none'
    convElement.style.display = 'block'
    convElement.innerHTML = '<div class="loader">Carregant...</div>'
    fetch('/fill_selected_call', requestOptions)
        .then(response => response.text())
        .then(data => {
            convElement.innerHTML = data;
        });
}

function submitRevision() {
    let amendments = document.querySelectorAll(".responseText");
    let fixedText = document.querySelectorAll(".fixedText");
    console.log(amendments)
    let amendmentData = {}
    let correctData = {}
    let fullRequest = {
        "amendments": amendmentData,
        "correct": correctData,
        "form": document.querySelector('input[name="conv_select"]:checked').value
    }
    for (let ii = 0; ii < amendments.length; ii++) {
        amendmentData[amendments[ii].id] = amendments[ii].value
    }
    for (let ii = 0; ii < fixedText.length; ii++) {
        correctData[fixedText[ii].id] = fixedText[ii].text
    }
    console.log(fullRequest)

    let requestOptions = {
        method: 'POST',
        redirect: 'follow',
        body: JSON.stringify(fullRequest),
        headers: {
            "Content-Type": "application/json",
          },
    };
    fetch('/esmenar/', requestOptions)
        .then(response => response.json())
        .then(data => {
            console.log(data)
            let responseKeys = Object.keys(data)
            for (let ii = 0; ii < responseKeys.length; ii++) {
                let new_element = document.createElement("p")
                new_element.innerText = data[responseKeys[ii]]
                document.getElementById(responseKeys[ii]).replaceWith(new_element)
                correctData[responseKeys[ii]] = data[responseKeys[ii]]
            }
        });
    let pdfData = {"text": correctData, "form": document.querySelector('input[name="conv_select"]:checked').value}
    let yetAnotherRequest = {
            method: 'POST',
            redirect: 'follow',
            body: JSON.stringify(pdfData),
            headers: {
                "Content-Type": "application/json",
            },
        };
    fetch('/get_pdf', yetAnotherRequest)
        .then(response => response.json())
        .then(data => {})
    document.getElementById("button_esmenes").display = "none"
}