const newCustomerUrl = 'https://mintic-bancoproj-g2.herokuapp.com/newCustomer';
//const newCustomerUrl = 'http://127.0.0.1:8000/newCustomer';

function validate_names(val) {
    const letters = /^[A-Z a-zÁÉÍÓÚáéíóúñ]+$/;
    if (val.match(letters))
        return true;
    else
        return false;
}

function validate_id(val) {
    if (Number(val) > 1000)
        return true;
    else
        return false;
}

function validate_password(val) {
    if (val.length >= 5)
        return true;
    else
        return false;
}

function collectData(evt) {
    evt.preventDefault();

    const id = document.registro.id.value;
    const firstName = document.registro.firstName.value.trim();
    const lastName = document.registro.lastName.value.trim();
    const email = document.registro.email.value.trim();
    const password = document.registro.password.value;

    let result = validate_id(id);
    if (!result) {
        alert('Cédula no es válida');
        return;
    }
    result = validate_names(firstName);
    if (!result) {
        alert('Nombre no es válido');
        return;
    }
    result = validate_names(lastName);
    if (!result) {
        alert('Apellido no es válido');
        return;
    }
    result = validate_password(password);
    if (!result) {
        alert('Contraseña no es válida. Debe tener al menos 5 caracteres.');
        return;
    }

    const customer = {
        id: id,
        firstName: firstName,
        lastName: lastName,
        email: email,
        password: password
    }
    console.log(customer);
    const dataToSend = JSON.stringify(customer);
    saveCustomer(dataToSend);
}

function saveCustomer(data) {
    // Petición HTTP
    fetch(newCustomerUrl, {
        method: "POST",
        headers: {
            "Content-Type": "text/json"
        },
        body: data
    })
        .then(response => {
            console.log(response);
            if (response.ok)
                return response.text()
            else
                throw new Error(response.text());
        })
        .then(data => {
            console.log(data);
            handleSuccess();
        })
        .catch(error => {
            console.error("ERROR: ", error.message);
            handleError();
        });
}

function handleSuccess() {
    document.getElementById("formData").remove();
    const message = document.createElement("p");
    message.innerText = "Cliente creado exitosamente.";
    const info = document.getElementById("info");
    info.appendChild(message);
}

function handleError() {
    document.getElementById("formData").remove();
    const message = document.createElement("p");
    message.innerText = "No se pudo crear el cliente. Intente luego.";
    const info = document.getElementById("info");
    info.appendChild(message);
}

// --------------------
document.registro.addEventListener("submit", collectData);