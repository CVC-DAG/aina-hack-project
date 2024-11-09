document.addEventListener("DOMContentLoaded", function() {
    let form = document.getElementById("url-form");
    form.preventDefault();
    console.log(form)

    form.addEventListener("submit", (event)=>{
        console.log("SUBMITTED")
        console.log(document.getElementById('#form-group').elements)
        document.getElementById('#form-group').innerHTML = "<h2>Hola, " + document.getElementById('#form-group').elements["url"] + ". Preparant la teva cita amb la ciència...</h2>"

        var requestOptions = {
            method: 'POST',
            body: formData,
            redirect: 'follow'
        };

        fetch('/submit_upload_business', requestOptions)
            .then(response => response.json())
            .then(data => {
                document.getElementById('#convocatories').innerText = data.message;
            });
        document.getElementById("#form-group").innerHTML = "<h2>Llest! Tria la convocatòria a la que vulguis aplicar.<\h2>"
    });
});


