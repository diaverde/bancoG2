const updateCustomerUrl = 'https://mintic-bancoproj-g2.herokuapp.com/updateCustomer/';
//const updateCustomerUrl = 'http://127.0.0.1:8000/updateCustomer/';

const userId = sessionStorage.getItem("clientId");

function validate_names(val) {
    const letters = /^[A-Z a-zÁÉÍÓÚáéíóúñ]+$/;
    if (val.match(letters))
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

    const firstName = document.actualizar.firstName.value.trim();
    const lastName = document.actualizar.lastName.value.trim();
    const email = document.actualizar.email.value.trim();
    const password = document.actualizar.password.value;

    let rasult = true;
    if (firstName) {
        let result = validate_names(firstName);
        if (!result) {
            alert('Nombre no es válido');
            return;
        }
    }
    if (lastName) {
        result = validate_names(lastName);
        if (!result) {
            alert('Apellido no es válido');
            return;
        }
    }
    if (password) {
        result = validate_password(password);
        if (!result) {
            alert('Contraseña no es válida. Debe tener al menos 5 caracteres.');
            return;
        }
    }

    const customer = {}
    if (firstName)
        customer.firstName = firstName;
    if (lastName)
        customer.lastName = lastName;
    if (email)
        customer.email = email;
    if (password)
        customer.password = password;
    console.log(customer);
    const dataToSend = JSON.stringify(customer);
    updateCustomer(dataToSend);
}

function updateCustomer(data) {
    const accessToken = sessionStorage.getItem("accessToken");
    // Petición HTTP
    fetch(updateCustomerUrl + userId, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + accessToken
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
            alert('Datos actualizados');
            goBack();
        })
        .catch(error => {
            console.error("ERROR: ", error.message);
            alert('Error al actualizar datos');
            goBack();
        });
}

function goBack() {
    window.location.href = './cliente.html?id=' + userId;
}

function showOldData() {
    const oldFName = sessionStorage.getItem('fname');
    const oldLName = sessionStorage.getItem('lname');
    const oldEmail = sessionStorage.getItem('email');

    document.actualizar.firstName.placeholder = oldFName;
    document.actualizar.lastName.placeholder = oldLName;
    document.actualizar.email.placeholder = oldEmail;
}

// --------------------
document.actualizar.addEventListener("submit", collectData);
document.addEventListener('DOMContentLoaded', showOldData);