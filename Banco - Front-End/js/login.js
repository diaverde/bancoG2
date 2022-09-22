//const loginUrl = 'https://mintic-bancoproj-g2.herokuapp.com/login';
const loginUrl = 'http://127.0.0.1:8000/login';

function collectData(evt) {
    evt.preventDefault();

    const email = document.login.email.value.trim();
    const password = document.login.password.value;

    const customer = {
        email: email,
        password: password
    }
    console.log(customer);
    const dataToSend = JSON.stringify(customer);
    console.log(dataToSend);
    login(dataToSend);
}

function login(data) {
    // Petición HTTP
    fetch(loginUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: data
    })
        .then(response => {
            console.log(response);
            if (response.ok || response.status == 401)
                return response.text()
            else
                throw new Error(response.text());
        })
        .then(data => {
            console.log(data);
            if (data.includes("Credenciales inválidas")) {
                handleError(data);
            }
            handleSuccess(JSON.parse(data));
        })
        .catch(error => {
            console.error("ERROR: ", error.message);
            handleError(error.message);
        });
}

function handleSuccess(data) {
    document.getElementById("formData").remove();
    const message = document.createElement("p");
    message.innerText = "Ingreso exitoso. Accediendo a su información...";
    const info = document.getElementById("info");
    info.appendChild(message);
    const token =
    {
        refresh: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY2Mzg5OTA4OCwiaWF0IjoxNjYzODEyNjg4LCJqdGkiOiI4NmY0OWEwY2M0ODc0MWRiYmRmMGUyY2VhZDQ1NzM1NiIsInVzZXJfaWQiOjQ0NTV9.YLGmEOudUlFOpchSDXZfLhKPvFbV77nxEYb0Nmj-Yqo",
        access: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjYzODEyOTg4LCJpYXQiOjE2NjM4MTI2ODgsImp0aSI6IjEyNTg2NWY4NjNmMzQ1OTFhZmJlMTIwN2QzZjg5YzM2IiwidXNlcl9pZCI6NDQ1NX0.IWnDKseoPz1tHZAWjdSSt-op4yKoRRmSEWNQ2RY4HKw"
    };
    console.log(data.access);
    console.log(data.refresh);
    sessionStorage.setItem("accessToken", token.access);
    sessionStorage.setItem("refreshToken", token.refresh);
    window.location.href = './cliente.html?id=' + data.id;
}

function handleError(err) {
    document.getElementById("formData").remove();
    const message = document.createElement("p");
    if (err)
        message.innerText = err;
    else
        message.innerText = "No se pudo ingresar. Intente luego.";
    const info = document.getElementById("info");
    info.appendChild(message);
}

// --------------------
document.login.addEventListener("submit", collectData);