const loginUrl = 'https://mintic-bancoproj-g2.herokuapp.com/login';
//const loginUrl = 'http://127.0.0.1:8000/login';

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
    //console.log(data.access);
    //console.log(data.refresh);
    sessionStorage.setItem("accessToken", data.access);
    sessionStorage.setItem("refreshToken", data.refresh);
    sessionStorage.setItem("clientId", data.id);
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