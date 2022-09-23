const getCustomerUrl = 'https://mintic-bancoproj-g2.herokuapp.com/getOneCustomer/';
//const getCustomerUrl = 'http://127.0.0.1:8000/getOneCustomer/';

function getCustomer() {
  const parsedUrl = new URL(window.location.href);
  //console.log(parsedUrl);
  const id = parsedUrl.searchParams.get("id");
  //console.log(id);
  const accessToken = sessionStorage.getItem("accessToken");
  const refreshToken = sessionStorage.getItem("refreshToken");
  console.log("Acá en el otro archivo: " + accessToken);
  console.log("Acá en el otro archivo: " + refreshToken);

  fetch(getCustomerUrl + id, {
    headers: {
      "Authorization": "Bearer " + accessToken
    }
  })
    .then(response => {
      console.log(response);
      if (response.ok || response.status == 400)
        return response.text()
      else
        throw new Error(response.status);
    })
    .then(data => {
      console.log("Datos: " + data);
      if (data.includes("No existe cliente con esa cédula")) {
        handleError(data);
      }
      customer = JSON.parse(data);
      handleCustomer(customer);
    })
    .catch(error => {
      console.error("ERROR: ", error.message);
      handleError();
    });
}

function handleCustomer(customer) {
  const accInfo = [];
  customer.accounts.forEach(acc => {
    const singleAccInfo = `
      <h4>Número de cuenta: ${acc.number}</h4>
      <h4>Saldo: ${acc.balance}</h4>`;
    accInfo.push(singleAccInfo);
  });
  const custDiv = document.createElement("div");
  custDiv.innerHTML = `
    <h3>Nombre: ${customer.firstName}</h3>
    <h3>Apellido: ${customer.lastName}</h3>
    <h3>Cédula: ${customer.id}</h3>
    <h3>Cuentas:</h3>`;
  accInfo.forEach(acc => custDiv.innerHTML += acc);
  document.getElementById("cargando").remove();
  const info = document.getElementById("info-customers");
  info.appendChild(custDiv);

  sessionStorage.setItem("fname", customer.firstName);
  sessionStorage.setItem("lname", customer.lastName);
  sessionStorage.setItem("email", customer.email);
}

function handleError(err) {
  document.getElementById("cargando").remove();
  const message = document.createElement("p");
  if (err)
    message.innerText = err;
  else
    message.innerText = "No se pudo cargar la información. Intente más tarde.";
  const info = document.getElementById("info-customers");
  info.appendChild(message);
}

//-----------------------------------

document.addEventListener("DOMContentLoaded", getCustomer);